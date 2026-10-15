# Reading a Search Console Export

Use this for Mode B, B-lite and C. Run `scripts/analyze_gsc.py` first; it does the arithmetic and grouping so judgment goes into interpretation.

## Getting the data
Ask for (or accept): Performance → Queries and Pages exports for the last 3 months, same date range, for the target URL (filter by page, then export queries). Compare with the previous period if the user has it. A CSV with columns like `Query/Top queries, Clicks, Impressions, CTR, Position` (any language of headers) works; Persian-header exports and Persian digits are handled by the script.

```
python scripts/analyze_gsc.py queries.csv                    # opportunities report (markdown)
python scripts/analyze_gsc.py queries.csv --json out.json    # also save machine-readable results
python scripts/analyze_gsc.py queries.csv --min-impressions 30 --brand "brandname,برند"
```

## How the script judges CTR
Rows whose queries differ only by Persian/Arabic letter variants or ZWNJ are merged first (impressions and clicks summed, position impression-weighted). It never uses an outside "average CTR by position" table, because those vary by niche, device, SERP features, and AI Overviews. Instead it builds a baseline from the user's own data: the impression-weighted CTR within each position bucket (1–3, 4–5, 6–10, 11–20, 21+) and flags queries well below that baseline with enough impressions to matter. Treat flags as hypotheses to check in the live SERP, not verdicts. Branded queries are separated so they do not hide non-brand problems.

## Interpreting the buckets
| Pattern | Likely cause | First action |
|---|---|---|
| Position 1–5, CTR far below own baseline | Title/snippet mismatch, SERP features or AI Overview absorbing the click, wrong intent | Open the live SERP for the query, compare titles/snippets, rewrite title + meta in the query's wording |
| Position 6–15, many impressions | Page is relevant but not the best answer | Add a standalone answer for the query, deepen the section, add internal links to the page |
| Position 11–30, rising impressions | Google is testing the page | Strengthen the exact-match section, entities, and internal links; do not rewrite the whole page |
| Many distinct queries sharing one URL, each tiny | Page is a broad hub without sections for each need | Map query clusters to new H2/H3 sections (below) |
| High impressions, zero clicks, position > 20 | Not really a visible ranking | Ignore in CTR analysis; consider a dedicated page if the intent is distinct |
| Query intent differs from page type (transactional query on an informational post or vice versa) | Intent mismatch | Reframe the page, or create/point to the right page; do not force both onto one URL |

Always check whether a drop or low CTR coincides with a SERP change (AI Overview, new feature) before blaming the page; compare the same queries before and after in the same device filter.

## Query → section mapping
1. Normalize (Persian/Arabic letters, digits, ZWNJ) and cluster queries by shared head terms and intent.
2. For each cluster with meaningful impressions, check whether the page has a heading that answers it. If not, add an H2/H3 phrased as the user would ask it, with a 1–3 sentence standalone answer first.
3. Take the highest-impression phrasing of the dominant cluster for the title and H1, as long as the result reads naturally.
4. Questions that appear in "People also ask" or in Search Console but have no heading are FAQ candidates only if the answer adds something the body does not.

## Title/meta rewrite procedure (B-lite)
1. Pull the top 5 queries by impressions for the URL and the current title/meta.
2. Identify the dominant intent and the wording that appears most.
3. Write 3 title options (≈ 50–60 characters, the key phrase early, a concrete benefit or qualifier, no clickbait) and 3 meta descriptions (≈ 120–155 characters: problem + promise + soft CTA only if natural). Lengths are rules of thumb: Google truncates by pixel width and rewrites titles/snippets often.
4. Keep H1, title, and URL aligned in meaning but not identical strings.
5. Tell the user to change one thing at a time where possible and re-measure after 3–4 weeks with the same date-range logic; otherwise attribution is impossible.

## What to report
- Summary of ranking queries (top by impressions, with position and CTR)
- Which flagged opportunities are real after a SERP check (or note they were not checked)
- Content gaps by cluster
- Priority list: title/meta → missing sections for high-impression clusters → depth/entities/internal links → tone and trust signals
- What cannot be concluded from the data
