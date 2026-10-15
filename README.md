# SEO + GEO Article Writer Skill

A skill for creating high-quality articles and deeply correcting published ones, built to rank in Google and be easy for AI answer engines to quote. Persian-first, multilingual capable, works for any topic.

It is deliberately honest about GEO: Google's own guidance says optimizing for its AI features is still SEO, so the skill puts effort into original content, clear structure, sourcing, and measurement, and does not sell tricks (llms.txt, special schema, guaranteed citations) that nobody has shown to work.

## What it does

- **Mode A:** new article, from research to Rank Math package
- **Mode B:** correct a published article using Search Console data
- **Mode B-lite:** title / meta / H1 fixes only
- **Mode C:** audit and priorities without a rewrite
- Search intent, semantic coverage, E-E-A-T (Who / How / Why), local SEO when relevant
- Standalone-answer writing for snippets and AI quoting
- Current schema guidance (Article, BreadcrumbList, LocalBusiness; FAQ/HowTo rich results are gone, see `references/schema-guide.md`)
- Persian typography and cliché control
- Scripts that do the arithmetic and structure checks instead of guessing

## Install

### Claude (Claude Code, claude.ai, Cowork)
- Claude Code: copy this folder to `~/.claude/skills/seo-geo-article-writer/` (or `.claude/skills/` in a project).
- claude.ai / Cowork: zip the folder so that `seo-geo-article-writer/SKILL.md` is at the top level of the archive and upload it as a skill.

### Grok
Place the folder in your Grok skills directory (for example `~/.grok/skills/seo-geo-article-writer/`). The `SKILL.md` front matter (`name`, `description`) is the common format; script execution depends on the tool's sandbox.

## Structure

```
seo-geo-article-writer/
├── SKILL.md                     workflow, modes, rules (the part loaded on trigger)
├── references/
│   ├── output-format.md         deliverable order
│   ├── geo-guide.md             what is and is not evidence-based for AI engines
│   ├── schema-guide.md          schema types, JSON-LD templates, deprecation timeline
│   ├── eeat-and-sources.md      Who/How/Why, sources, claim labels, YMYL
│   ├── persian-writing.md       typography, ZWNJ, tone, cliché list
│   ├── search-console-analysis.md  reading an export, title/meta procedure
│   ├── correction-patterns.md   Mode B failure modes and fixes
│   ├── rank-math-templates.md   Rank Math fields and formulas
│   ├── checklists.md            research, quality, structure, delivery
│   └── examples.md              before/after examples
├── scripts/
│   ├── analyze_gsc.py           Search Console CSV → opportunities (stdlib only)
│   └── lint_article.py          article HTML checks (stdlib only)
└── evals/evals.json             prompts for testing the skill
```

## Scripts

```bash
# Search Console export (English or Persian headers/digits)
python scripts/analyze_gsc.py queries.csv --brand "brand,برند" --min-impressions 30 --json out.json

# Article HTML
python scripts/lint_article.py article.html --focus "focus phrase" --title "SEO title" --meta "meta description" --strict
```

Both need only Python 3. Their thresholds are heuristics that tell you where to look; they are not ranking rules.

## Keeping it current
SEO and AI-search guidance changes quickly (for example Google removed FAQ rich results in May 2026). `geo-guide.md` and `schema-guide.md` carry a "last checked" date; re-verify them against Google Search Central before relying on them after a few months.

## Origin
Extracted and generalized from production prompts used for renomarkazi.com content operations, then extended with sourced guidance, scripts, and tests.

License: Use freely for your own projects.
