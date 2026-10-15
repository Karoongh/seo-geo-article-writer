#!/usr/bin/env python3
"""Analyze a Google Search Console performance export (CSV) for SEO opportunities.

Standard library only. Handles English and Persian headers, Persian/Arabic digits,
percent CTR strings, and Persian/Arabic letter variants in queries.

Usage:
  python analyze_gsc.py queries.csv
  python analyze_gsc.py queries.csv --json out.json --min-impressions 30 --brand "brand,برند"

CTR is judged against a baseline built from the user's own data (impression-weighted
CTR per position bucket), not an outside average table. Flags are hypotheses to check
in the live SERP, not verdicts.
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

HEADER_ALIASES = {
    "dimension": ["query", "queries", "top queries", "page", "pages", "top pages", "url",
                  "عبارت", "پرسش", "کوئری", "کوئری‌های برتر", "صفحه", "صفحات برتر", "پرس‌وجو"],
    "clicks": ["clicks", "click", "کلیک", "کلیک‌ها"],
    "impressions": ["impressions", "impression", "نمایش", "نمایش‌ها", "ایمپرشن"],
    "ctr": ["ctr", "click-through rate", "نرخ کلیک", "نرخ کلیک به نمایش"],
    "position": ["position", "average position", "avg position", "avg. position", "رتبه",
                 "جایگاه", "موقعیت", "میانگین رتبه", "میانگین جایگاه", "موقعیت متوسط"],
}

STOPWORDS = set("""
از در به با برای که این آن را و یا تا چه چی چرا چطور چگونه کدام آیا است هست می چیست یعنی شد شده میشه می‌شود باید
    
the a an of to in for on and or is are what why how does do my i
""".split())

BUCKETS = [(1, 3, "1-3"), (4, 5, "4-5"), (6, 10, "6-10"), (11, 20, "11-20"), (21, 10**6, "21+")]
BUCKET_LIMITS = [(4, "1-3"), (6, "4-5"), (11, "6-10"), (21, "11-20")]  # position < limit -> bucket


def normalize_digits(s):
    return s.translate(str.maketrans(PERSIAN_DIGITS + ARABIC_DIGITS, "0123456789" * 2))


def normalize_text(s):
    s = s.replace("ي", "ی").replace("ك", "ک").replace("‌", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def parse_number(raw):
    """Parse numbers like '1,234', '۱٬۲۳۴', '3.5', '3,5', '1.5%' -> float (percent -> fraction handled by caller)."""
    if raw is None:
        return None
    s = normalize_digits(str(raw)).strip()
    s = s.replace("٬", "").replace("٫", ".").replace(" ", "").replace(" ", "")
    pct = s.endswith("%") or s.endswith("٪")
    s = s.rstrip("%٪")
    if not s or s in ("-", "—"):
        return None
    # decide on comma: thousands separator if pattern like 1,234 or 12,345,678
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    else:
        s = s.replace(",", ".")
    try:
        v = float(s)
    except ValueError:
        return None
    return v / 100.0 if pct else v


def sniff_dialect(text):
    try:
        return csv.Sniffer().sniff(text[:4096], delimiters=",;\t")
    except csv.Error:
        return csv.excel


def map_headers(headers):
    mapping = {}
    norm = [normalize_text(h) for h in headers]
    for key, aliases in HEADER_ALIASES.items():
        al = [normalize_text(a) for a in aliases]
        for i, h in enumerate(norm):
            if h in al and key not in mapping:
                mapping[key] = i
    if "dimension" not in mapping and headers:
        # fall back: first column that is not a mapped metric
        used = set(mapping.values())
        for i in range(len(headers)):
            if i not in used:
                mapping["dimension"] = i
                break
    return mapping


def load_rows(path):
    with open(path, "rb") as fh:
        data = fh.read()
    for enc in ("utf-8-sig", "utf-16", "cp1256", "latin-1"):
        try:
            text = data.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    dialect = sniff_dialect(text)
    reader = csv.reader(io.StringIO(text), dialect)
    rows = [r for r in reader if any(c.strip() for c in r)]
    if len(rows) < 2:
        raise SystemExit("error: CSV has no data rows")
    headers = rows[0]
    mapping = map_headers(headers)
    missing = [k for k in ("dimension", "impressions", "position") if k not in mapping]
    if missing:
        raise SystemExit(
            f"error: could not find columns for {missing}. Headers seen: {headers}. "
            "Expected Query/Page, Clicks, Impressions, CTR, Position (English or Persian).")
    out = []
    skipped = 0
    for r in rows[1:]:
        def cell(key):
            i = mapping.get(key)
            return r[i] if i is not None and i < len(r) else None
        imp = parse_number(cell("impressions"))
        pos = parse_number(cell("position"))
        if imp is None or pos is None:
            skipped += 1
            continue
        clicks = parse_number(cell("clicks"))
        ctr = parse_number(cell("ctr"))
        if clicks is None and ctr is not None:
            clicks = ctr * imp
        if ctr is None:
            ctr = (clicks / imp) if (clicks is not None and imp) else 0.0
        if clicks is None:
            clicks = 0.0
        # CTR given as 1.5 (meaning percent) without % sign: detect if > 1 while clicks<=imp
        if ctr > 1 and imp:
            ctr = clicks / imp
        out.append({"query": (cell("dimension") or "").strip(), "norm": normalize_text(cell("dimension") or ""),
                    "clicks": clicks, "impressions": imp, "ctr": ctr, "position": pos})
    return merge_variants(out), skipped


def merge_variants(rows):
    """Merge rows whose queries are identical after Persian/Arabic and ZWNJ normalization."""
    merged = {}
    for r in rows:
        key = r["norm"]
        if key not in merged:
            merged[key] = {**r, "_pw": r["position"] * r["impressions"], "variants": 1}
        else:
            m = merged[key]
            m["clicks"] += r["clicks"]
            m["impressions"] += r["impressions"]
            m["_pw"] += r["position"] * r["impressions"]
            m["variants"] += 1
    out = []
    for m in merged.values():
        if m["impressions"]:
            m["position"] = m["_pw"] / m["impressions"]
            m["ctr"] = m["clicks"] / m["impressions"]
        del m["_pw"]
        out.append(m)
    return out


def bucket_of(pos):
    for limit, name in BUCKET_LIMITS:
        if pos < limit:
            return name
    return "21+"


def tokens(norm):
    return [t for t in re.split(r"[^\w؀-ۿ]+", norm) if t and t not in STOPWORDS and len(t) > 1]


def build_baseline(rows):
    agg = defaultdict(lambda: [0.0, 0.0])
    for r in rows:
        b = bucket_of(r["position"])
        agg[b][0] += r["clicks"]
        agg[b][1] += r["impressions"]
    return {b: (c / i if i else 0.0) for b, (c, i) in agg.items()}, {b: i for b, (c, i) in agg.items()}


def cluster(rows):
    weight = defaultdict(float)
    for r in rows:
        for t in set(tokens(r["norm"])):
            weight[t] += r["impressions"]
    groups = defaultdict(list)
    for r in rows:
        toks = tokens(r["norm"])
        if not toks:
            groups["(other)"].append(r)
            continue
        head = max(toks, key=lambda t: (weight[t], len(t)))
        groups[head].append(r)
    result = []
    for head, items in groups.items():
        imp = sum(i["impressions"] for i in items)
        clk = sum(i["clicks"] for i in items)
        pos = sum(i["position"] * i["impressions"] for i in items) / imp if imp else 0
        result.append({"head": head, "queries": len(items), "impressions": imp, "clicks": clk,
                       "ctr": clk / imp if imp else 0, "position": pos,
                       "top": [i["query"] for i in sorted(items, key=lambda x: -x["impressions"])[:3]]})
    return sorted(result, key=lambda g: -g["impressions"])


def pct(x):
    return f"{x * 100:.1f}%"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv_path")
    ap.add_argument("--min-impressions", type=int, default=20, help="ignore rows below this for flags (default 20)")
    ap.add_argument("--brand", default="", help="comma-separated brand terms to separate branded queries")
    ap.add_argument("--ratio", type=float, default=0.5, help="flag CTR below ratio x bucket baseline (default 0.5)")
    ap.add_argument("--top", type=int, default=15, help="rows per table (default 15)")
    ap.add_argument("--json", dest="json_path", help="write results to this JSON file")
    args = ap.parse_args()

    rows, skipped = load_rows(args.csv_path)
    brand_terms = [normalize_text(b) for b in args.brand.split(",") if b.strip()]

    def is_brand(r):
        return any(b in r["norm"] for b in brand_terms)

    branded = [r for r in rows if brand_terms and is_brand(r)]
    non_brand = [r for r in rows if not (brand_terms and is_brand(r))]

    baseline, bucket_imps = build_baseline(non_brand)
    total_imp = sum(r["impressions"] for r in rows)
    total_clk = sum(r["clicks"] for r in rows)

    flagged = []
    for r in non_brand:
        if r["impressions"] < args.min_impressions or r["position"] > 20:
            continue
        b = bucket_of(r["position"])
        base = baseline.get(b, 0)
        if base > 0 and r["ctr"] < base * args.ratio:
            lost = (base - r["ctr"]) * r["impressions"]
            flagged.append({**r, "bucket": b, "baseline_ctr": base, "est_missed_clicks": lost})
    flagged.sort(key=lambda x: -x["est_missed_clicks"])

    near = [r for r in non_brand if 6 <= r["position"] <= 20 and r["impressions"] >= args.min_impressions]
    near.sort(key=lambda x: -x["impressions"])

    zero = [r for r in non_brand if r["clicks"] == 0 and r["impressions"] >= args.min_impressions and r["position"] <= 10]
    zero.sort(key=lambda x: -x["impressions"])

    clusters = cluster(non_brand)

    L = []
    L.append("# Search Console analysis")
    L.append(f"Rows: {len(rows)} (skipped unparsable: {skipped}) | impressions: {int(total_imp)} | clicks: {int(total_clk)} | overall CTR: {pct(total_clk / total_imp if total_imp else 0)}")
    if brand_terms:
        bi = sum(r["impressions"] for r in branded)
        bc = sum(r["clicks"] for r in branded)
        L.append(f"Branded rows: {len(branded)} ({int(bi)} impressions, {int(bc)} clicks); excluded from baselines and flags")
    L.append("\n## Baseline CTR by position bucket (from this file, non-brand)")
    L.append("| Bucket | Impressions | Baseline CTR |")
    L.append("|---|---|---|")
    for _, _, name in BUCKETS:
        if name in baseline:
            L.append(f"| {name} | {int(bucket_imps[name])} | {pct(baseline[name])} |")
    if all(bucket_imps.get(n, 0) < 100 for _, _, n in BUCKETS):
        L.append("\nWarning: very few impressions; baselines are noisy. Use a longer date range if possible.")

    L.append(f"\n## CTR well below baseline (ratio < {args.ratio}, impressions >= {args.min_impressions}, position <= 20)")
    if flagged:
        L.append("| Query | Impr. | Pos. | CTR | Baseline | Est. missed clicks |")
        L.append("|---|---|---|---|---|---|")
        for r in flagged[:args.top]:
            L.append(f"| {r['query']} | {int(r['impressions'])} | {r['position']:.1f} | {pct(r['ctr'])} | {pct(r['baseline_ctr'])} | {r['est_missed_clicks']:.0f} |")
    else:
        L.append("None flagged.")

    L.append("\n## Position 6-20 with meaningful impressions (depth / internal-link candidates)")
    if near:
        L.append("| Query | Impr. | Pos. | CTR |")
        L.append("|---|---|---|---|")
        for r in near[:args.top]:
            L.append(f"| {r['query']} | {int(r['impressions'])} | {r['position']:.1f} | {pct(r['ctr'])} |")
    else:
        L.append("None.")

    L.append("\n## Top-10 position but zero clicks (check snippet and live SERP)")
    if zero:
        for r in zero[:args.top]:
            L.append(f"- {r['query']}: {int(r['impressions'])} impressions, position {r['position']:.1f}")
    else:
        L.append("None.")

    L.append("\n## Query clusters (by dominant head term; review manually)")
    L.append("| Head term | Queries | Impr. | Clicks | CTR | Avg pos. | Examples |")
    L.append("|---|---|---|---|---|---|---|")
    for g in clusters[:args.top]:
        L.append(f"| {g['head']} | {g['queries']} | {int(g['impressions'])} | {int(g['clicks'])} | {pct(g['ctr'])} | {g['position']:.1f} | {'; '.join(g['top'])} |")

    L.append("\n## Reading notes")
    L.append("- Flags are hypotheses: open the live SERP for each flagged query (AI Overview, features, competitors) before rewriting.")
    L.append("- Cluster heads are heuristic token groupings; merge or split by judgment and map each cluster to a heading.")
    L.append("- Position is an average and varies by device/country; filter to one device and country for fair comparisons.")
    report = "\n".join(L)
    print(report)

    if args.json_path:
        payload = {
            "totals": {"rows": len(rows), "impressions": total_imp, "clicks": total_clk,
                       "ctr": total_clk / total_imp if total_imp else 0},
            "baseline_ctr": baseline,
            "ctr_below_baseline": [{k: v for k, v in r.items() if k != "norm"} for r in flagged],
            "position_6_20": [{k: v for k, v in r.items() if k != "norm"} for r in near],
            "top10_zero_clicks": [{k: v for k, v in r.items() if k != "norm"} for r in zero],
            "clusters": clusters,
        }
        with open(args.json_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
