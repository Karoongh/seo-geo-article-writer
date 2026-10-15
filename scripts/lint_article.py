#!/usr/bin/env python3
"""Lint an article's HTML for structure, Persian typography, and common SEO/GEO slips.

Standard library only. Output is a list of ERROR / WARN / INFO lines. The checks are
heuristics meant to make you look, not laws: judge each finding in context.

Usage:
  python lint_article.py article.html --focus "علت چراغ X" --title "..." --meta "..."
  python lint_article.py article.html --strict     # exit code 1 if any ERROR
"""
import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser

PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

CLICHES = [
    "در دنیای امروز", "امروزه", "در این مقاله قصد داریم", "در این مقاله به بررسی",
    "همان طور که می دانید", "همان‌طور که می‌دانید", "همانطور که می‌دانید",
    "بدون شک", "بی تردید", "بی‌تردید", "در پایان باید گفت", "به طور خلاصه می توان گفت",
    "در عصر حاضر", "یکی از مهم ترین", "یکی از مهم‌ترین",
]
OVERCLAIMS = ["تضمینی", "۱۰۰٪", "100%", "بهترین در ایران", "بی‌نظیر", "بدون رقیب", "تضمین می‌کنیم", "تضمین می کنیم"]
GENERIC_ANCHORS = ["اینجا", "کلیک کنید", "ادامه مطلب", "بیشتر بخوانید", "click here", "here", "read more"]
FAQ_MARKERS = ["سوالات متداول", "سؤالات متداول", "پرسش‌های متداول", "پرسش های متداول", "faq"]
SKIP_TAGS = {"script", "style", "code", "pre", "noscript"}


def norm(s):
    s = s.replace("ي", "ی").replace("ك", "ک").replace("‌", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings = []      # (level, text)
        self.paragraphs = []    # text
        self.imgs = []          # (src, alt or None)
        self.links = []         # (href, text)
        self.text_parts = []
        self.in_heading = None
        self.heading_buf = []
        self.in_p = False
        self.p_buf = []
        self.in_a = None
        self.a_buf = []
        self.skip = 0
        self.has_rtl = False
        self.first_p_after_h1 = None
        self._seen_h1 = False
        self.json_ld = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP_TAGS:
            if tag == "script" and "ld+json" in (a.get("type") or ""):
                self.json_ld += 1
            self.skip += 1
            return
        if a.get("dir", "").lower() == "rtl":
            self.has_rtl = True
        if re.fullmatch(r"h[1-6]", tag):
            self.in_heading = int(tag[1])
            self.heading_buf = []
        elif tag == "p":
            self.in_p = True
            self.p_buf = []
        elif tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt")))
        elif tag == "a":
            self.in_a = a.get("href", "")
            self.a_buf = []

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
            return
        if re.fullmatch(r"h[1-6]", tag) and self.in_heading:
            text = "".join(self.heading_buf).strip()
            self.headings.append((self.in_heading, text))
            if self.in_heading == 1:
                self._seen_h1 = True
            self.in_heading = None
        elif tag == "p" and self.in_p:
            text = "".join(self.p_buf).strip()
            self.paragraphs.append(text)
            if self._seen_h1 and self.first_p_after_h1 is None and text:
                self.first_p_after_h1 = text
            self.in_p = False
        elif tag == "a" and self.in_a is not None:
            self.links.append((self.in_a, "".join(self.a_buf).strip()))
            self.in_a = None

    def handle_data(self, data):
        if self.skip:
            return
        self.text_parts.append(data)
        if self.in_heading:
            self.heading_buf.append(data)
        if self.in_p:
            self.p_buf.append(data)
        if self.in_a is not None:
            self.a_buf.append(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("html_path")
    ap.add_argument("--focus", default="", help="focus keyword/phrase")
    ap.add_argument("--title", default="", help="SEO title to check")
    ap.add_argument("--meta", default="", help="meta description to check")
    ap.add_argument("--site", default="", help="site domain (e.g. example.com) to classify internal links")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any ERROR")
    args = ap.parse_args()

    with open(args.html_path, "rb") as fh:
        raw = fh.read()
    try:
        html = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        html = raw.decode("cp1256", errors="replace")

    d = Doc()
    d.feed(html)
    text = " ".join(d.text_parts)
    ntext = norm(text)
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    out = []

    def add(level, msg):
        out.append((level, msg))

    # --- structure
    h1s = [h for h in d.headings if h[0] == 1]
    if len(h1s) == 0:
        add("ERROR", "No H1 found.")
    elif len(h1s) > 1:
        add("ERROR", f"{len(h1s)} H1 tags found; use exactly one (WordPress themes often add their own: check the page source).")
    prev = 0
    for lvl, t in d.headings:
        if not t:
            add("ERROR", f"Empty H{lvl}.")
        if prev and lvl > prev + 1:
            add("WARN", f"Heading level jumps from H{prev} to H{lvl} at «{t[:50]}».")
        prev = lvl
    ncount = Counter(norm(t) for _, t in d.headings if t)
    for t, c in ncount.items():
        if c > 1:
            add("WARN", f"Duplicate heading text ({c}x): «{t[:60]}».")
    if len(d.headings) < 3:
        add("WARN", "Fewer than 3 headings; long articles need navigable sections.")

    # --- paragraphs / readability
    long_ps = [p for p in d.paragraphs if len(p.split()) > 110]
    if long_ps:
        add("WARN", f"{len(long_ps)} paragraph(s) over ~110 words; consider splitting for mobile readability.")
    if d.paragraphs:
        avg = sum(len(p.split()) for p in d.paragraphs) / len(d.paragraphs)
        add("INFO", f"{len(words)} words, {len(d.paragraphs)} paragraphs (avg {avg:.0f} words).")

    # --- images and links
    for src, alt in d.imgs:
        if alt is None or not alt.strip():
            add("WARN", f"Image without ALT text: {src[:70] or '(no src)'}.")
    ext = inn = 0
    for href, label in d.links:
        is_ext = href.startswith("http") and (not args.site or args.site not in href)
        if is_ext:
            ext += 1
        else:
            inn += 1
        if norm(label) in [norm(a) for a in GENERIC_ANCHORS]:
            add("WARN", f"Generic link anchor «{label}» → {href[:60]}; use a descriptive anchor.")
    add("INFO", f"Links: {inn} internal/relative, {ext} external, {len(d.imgs)} images, {d.json_ld} JSON-LD block(s).")
    if inn == 0:
        add("WARN", "No internal links found.")

    # --- Persian typography
    if re.search(r"[يك]", text):
        add("ERROR", "Arabic ي/ك characters present; replace with Persian ی/ک.")
    mi = re.findall(r"(?<![؀-ۿ])(ن?می) (?=[؀-ۿ]{2,})", text)
    if mi:
        add("WARN", f"{len(mi)} possible «می/نمی» followed by a space instead of ZWNJ (e.g. «می کنم» → «می‌کنم»).")
    pl = re.findall(r"[؀-ۿ] (ها|های)(?![؀-ۿ])", text)
    if pl:
        add("WARN", f"{len(pl)} possible plural «ها/های» after a space instead of ZWNJ.")
    mixed = re.findall(r"(?:[0-9]+[" + PERSIAN_DIGITS + ARABIC_DIGITS + r"]|[" + PERSIAN_DIGITS + ARABIC_DIGITS + r"]+[0-9])[0-9" + PERSIAN_DIGITS + ARABIC_DIGITS + r"]*", text)
    if mixed:
        add("WARN", f"{len(mixed)} number(s) mixing Persian and Latin digits, e.g. «{mixed[0]}».")
    n_fa = len(re.findall("[" + PERSIAN_DIGITS + "]", text))
    n_en = len(re.findall(r"[0-9]", text))
    if n_fa and n_en:
        add("INFO", f"Digit styles on page: {n_fa} Persian, {n_en} Latin (fine if Latin is for codes/models/units; keep it deliberate).")
    if re.search(r"[؀-ۿ]", text) and not d.has_rtl and "dir=" not in html.lower():
        add("INFO", "No dir=\"rtl\" found in the HTML; fine if the theme sets it, otherwise add it to the article container.")

    # --- cliches and overclaims
    for c in CLICHES:
        if norm(c) in ntext:
            add("WARN", f"Cliché/filler phrase: «{c}».")
    for c in OVERCLAIMS:
        if norm(c) in ntext:
            add("WARN", f"Unproven superlative/guarantee claim: «{c}»; remove or support it.")
    if d.first_p_after_h1:
        fp = norm(d.first_p_after_h1)
        for c in CLICHES:
            if fp.startswith(norm(c)):
                add("ERROR", f"Introduction starts with a generic opener: «{c}».")

    # --- placeholders and unverified claims
    ph = re.findall(r"\[TO CONFIRM[^\]]*\]|TODO|XXX|لورم", html, flags=re.I)
    if ph:
        add("ERROR", f"{len(ph)} unresolved placeholder(s) in the HTML (e.g. {ph[0]}). Resolve before publishing.")

    # --- FAQ
    faq_idx = next((i for i, (_, t) in enumerate(d.headings) if any(m in norm(t) for m in [norm(x) for x in FAQ_MARKERS])), None)
    if faq_idx is not None:
        before = {norm(t) for _, t in d.headings[:faq_idx]}
        qs = [t for _, t in d.headings[faq_idx + 1:]]
        dup = [q for q in qs if norm(q) in before]
        if dup:
            add("WARN", f"FAQ question(s) repeat earlier headings: {', '.join('«'+q[:40]+'»' for q in dup)}.")
        if not qs:
            add("WARN", "FAQ heading present but no questions as sub-headings.")
    if re.search(r'"@type"\s*:\s*"(FAQPage|HowTo)"', html):
        add("INFO", "FAQPage/HowTo JSON-LD present: Google shows no rich result for these (FAQ removed May 2026, HowTo 2023). Keep only if it mirrors visible content.")

    # --- focus keyword
    if args.focus:
        fk = norm(args.focus)
        n = ntext.count(fk)
        density = (n * max(1, len(fk.split()))) / max(1, len(words)) * 100
        add("INFO", f"Focus «{args.focus}»: {n} occurrence(s), ~{density:.2f}% of words.")
        if n == 0:
            add("WARN", "Focus phrase never appears exactly; check spelling/ZWNJ variants or use a natural close variant deliberately.")
        if density > 2.5 and len(words) >= 150:
            add("WARN", "Focus phrase density looks high; check for mechanical repetition.")
        in_h1 = any(fk in norm(t) for _, t in h1s)
        if not in_h1:
            add("INFO", "Focus phrase not in the H1 (acceptable if the H1 uses the natural variant users type).")
        sub = [t for l, t in d.headings if l in (2, 3)]
        hit = sum(1 for t in sub if fk in norm(t))
        if sub and hit / len(sub) > 0.5 and len(sub) >= 4:
            add("WARN", f"Focus phrase appears in {hit} of {len(sub)} H2/H3 headings; looks over-optimized.")
        first100 = norm(" ".join(words[:100]))
        if fk not in first100:
            add("INFO", "Focus phrase not in the first ~100 words (only matters if it fits naturally).")

    # --- title/meta
    if args.title:
        L = len(args.title)
        lvl = "WARN" if (L > 65 or L < 25) else "INFO"
        add(lvl, f"SEO title length {L} chars (rule of thumb 50-60; Google truncates by pixel width).")
    if args.meta:
        L = len(args.meta)
        lvl = "WARN" if (L > 160 or L < 70) else "INFO"
        add(lvl, f"Meta description length {L} chars (rule of thumb ~120-155).")

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    out.sort(key=lambda x: order[x[0]])
    for lvl, msg in out:
        print(f"{lvl}: {msg}")
    errs = sum(1 for l, _ in out if l == "ERROR")
    warns = sum(1 for l, _ in out if l == "WARN")
    print(f"\nSummary: {errs} error(s), {warns} warning(s).")
    if args.strict and errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
