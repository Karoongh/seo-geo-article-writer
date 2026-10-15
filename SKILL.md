---
name: seo-geo-article-writer
description: Write new SEO + GEO articles (Persian-first, multilingual capable) or deeply rewrite published articles that underperform. Use whenever the user wants an article, blog post, or service/landing-page copy that should rank on Google and be quoted by AI answer engines (ChatGPT, Gemini, AI Overviews, Perplexity), or shares an existing URL/post with Search Console data (impressions, clicks, CTR, position) to fix. Also trigger for Rank Math setup (focus keyword, title, meta, schema, slug), schema/JSON-LD for articles, search-intent or competitor-gap analysis, title/meta rewrites for low CTR, and Persian requests such as "مقاله بنویس"، "سئو"، "اصلاح مقاله"، "ایمپرشن بالا کلیک کم"، "رنک مت". Use it even if the user never says "SEO" but wants content that must perform in search.
---

# SEO + GEO Article Writer & Corrector

The goal is content that is accurate, human, and citable: it answers the searcher fast, ranks in Google, and is easy for AI answer engines to quote. Rank Math green scores and word counts are side effects, never the target; chasing them produces padded, robotic text that readers and AI systems both discount.

Keep one fact in mind throughout: Google's own guidance (May 2026) says optimizing for AI features "is still SEO". There is no special markup, file, or chunking trick that Google asks for. So the work is: original useful content, clean structure, crawlable and indexable pages, honest sourcing. Other engines (ChatGPT, Perplexity, Gemini) may weigh signals differently and no one outside them knows exactly how, so never promise citations. Details and the evidence status of each tactic: `references/geo-guide.md`.

## Pick the mode

- **Mode A, new article.** Input: a topic (plus optional business context).
- **Mode B, correct an existing article.** Input: URL or full text, ideally with Search Console data (queries, impressions, clicks, CTR, position) and the current title/meta.
- **Mode B-lite, title/meta/H1 only.** When the user only wants a CTR fix, skip the full rewrite: diagnose, give 3 title/meta options, and say what else would be worth changing.
- **Mode C, audit only.** The user wants a verdict or priority list without a rewrite.

Other requests inside the skill's scope: if the user asks for `llms.txt` or other AI-specific files, do not build them by default. Say they are harmless but unproven (Google ignores them) and produce a minimal one only if the user still wants it.

If the user gives a URL, fetch it with WebFetch. If they attach a Search Console export, run `<skill folder>/scripts/analyze_gsc.py` on it instead of eyeballing rows (see `references/search-console-analysis.md`). If inputs are missing, proceed with what exists and state what the diagnosis could not cover; ask only if the topic itself is unclear. If the user demands a guarantee (of rankings, of AI citations), decline the guarantee in two sentences, say what you can do instead, and carry on with the task.

## Workflow

### 1. Intake (30 seconds, silently)
Identify: language and dialect, topic or existing article, business context (name, site, location, services, contact channels), real experience notes the business supplied, related internal pages, existing brand/tone rules. Whatever the user did not supply stays unknown; never fill it with invention.

### 2. Research before writing
Use WebSearch/WebFetch; do not write from memory alone. Establish:
- Primary and secondary search intent, funnel stage
- Real user questions and the exact phrases people type (including Latin-script terms seen on screens, labels, error messages)
- Key entities and related concepts
- Competitor gaps: what top-ranking pages miss in depth, answers, structure, CTA, and what they get wrong. Some sites refuse automated fetching (robots or legal blocks). Do not route around a refusal with mirrors or caches; build the gap analysis from what the search results show (titles, snippets, visible headings, People-also-ask style questions) and say in the report that those pages were not read in full.
- Sources, in this order: official docs and standards bodies → manufacturers / peer-reviewed or highly reputable technical sources → expert sites → forums only as a weak supporting signal

If only foreign-language or other-market sources can be opened (for example a Persian-language topic where the best primary sources are English manuals), use them, say which market or model they cover, and do not generalize beyond it. Persian-first applies to the writing, not to the evidence.

Never invent codes, prices, durations, statistics, or technical facts. Label every claim by what it is: official fact, practitioner experience, probable cause, confirmed cause, user report. Experience claims ("in our workshop we always see…") are allowed only if the user supplied them. Source rules and YMYL handling: `references/eeat-and-sources.md`.

For Mode B, diagnose first (`references/correction-patterns.md`).

### 3. Design the structure
One H1. H2/H3 are the real questions users ask. For problem/fault/service topics the default flow is meaning → symptoms → probable causes → how to diagnose → solutions → when to see a professional → cost factors → FAQ; adapt for informational, comparison, and how-to intent (`references/checklists.md`). Do not change a working URL without strong reason.

### 4. Write
- Open with 1–3 paragraphs that name the problem and promise concrete answers. No generic openers.
- Start each important section with a short standalone answer (1–3 sentences) that still makes sense when quoted alone, then explain, then give next steps. This helps hurried readers, featured snippets, and AI quoting alike; it is not a trick, so do not cut real depth to achieve it.
- Add something no competitor page has: original comparison, a decision table, a diagnostic order, a real number the user supplied, a correction of a common myth. Google calls generic recycled content "commodity", and it is what AI systems can already produce, so it earns nothing.
- Voice: natural, varied sentence length, the terms practitioners and customers really use. For Persian, follow `references/persian-writing.md` (typography, ZWNJ, tone, banned clichés).
- Cover related entities naturally; no keyword stuffing.
- On topics with risk (vehicles, health, electricity, structure, legal, finance), state dangers plainly and mark the limits of remote diagnosis. Do not give oversimplified dangerous instructions.
- CTA only after value is delivered, matched to intent, never on every H2. For local businesses weave location and contact (only channels the user gave) into CTA and service sections, not every paragraph. With no contact details supplied, write a short generic CTA («برای بررسی دقیق با تعمیرگاه تماس بگیرید») and list the missing contact details under "needs your confirmation"; never invent a phone number, address, years of experience, or service list.
- Links: internal links use only URLs the user gave or that you verified on their site, with natural anchors; external links go only to high-authority sources. If you have none, leave links out of the HTML and give suggested internal-link targets and anchors in the report; the linter's "no internal links" warning is then expected.
- Images: propose realistic images with natural ALT text. Never present AI-generated images as real photos of the business or its work.
- FAQ: only questions that add new value, each answer independent, never a rewording of an H2. FAQ is for readers; it no longer produces a Google rich result (see schema below).

### 5. Check before delivering
Save the article HTML and run `python <skill folder>/scripts/lint_article.py article.html --focus "<focus keyword>" [--title ... --meta ...]` (use the absolute path of this skill's folder; the working directory is usually not the skill folder). Fix real findings; the linter's heuristics (keyword density, paragraph length) are prompts to look, not laws. Then read the draft as four readers:
1. The user: did I get my answer on the first screen?
2. The domain expert: any wrong or dangerously simplified claim?
3. The SEO: intent coverage, headings, entities, links, title/meta?
4. The AI engine: can each section stand alone as a clean 1–3 sentence answer?

For high-stakes pages, have an independent agent that has not seen the drafting fact-check the claims against the sources. High-stakes means medical, legal, financial, and safety-critical vehicle or electrical topics (brakes, airbags, steering, fuel, battery/high voltage). If you cannot spawn an agent, do a separate verification pass against the opened sources and write in the final check that it was not independent.

**Placeholders and gaps.** The HTML must be publishable as it stands: where a fact is missing, omit the sentence or write the safe general version, and list what needs confirming in the report. The only exception is a contact or author field the user must fill in; mark it `[TO CONFIRM: …]` so the linter blocks publishing until it is resolved.

## Schema: what to recommend now
Recommend `Article` or `BlogPosting` (with real author, dates, image) plus `BreadcrumbList`, and `LocalBusiness`/`Organization` where true. Do not promise FAQ or HowTo rich results: Google dropped HowTo in 2023 and removed FAQ rich results entirely in May 2026. FAQPage markup is still valid schema.org and harmless if it matches visible content, but present it as optional. Templates and the dated timeline: `references/schema-guide.md`.

## Deliverable
Write the final text in the user's language (Persian by default if they write Persian). Use the order in `references/output-format.md` (analysis → structure → article → CTAs → FAQ → Rank Math package → images → final check). Keep the analysis proportional to the task; a tight one beats a long generic one.

Deliver the article as a file the user can open: clean WordPress-ready HTML (`<h1>`, `<h2>`, `<h3>`, `<p>`, lists, tables, `<strong>`), saved as `.html` and sent with SendUserFile (or as a document if the session offers a Docs type; if nothing can send files, leave it in the working directory and state the path). The article's FAQ lives inside the HTML; section 5 of the report need not copy it, only note the schema decision. Put the research summary, CTAs, Rank Math package, and final check in the chat reply or a second file so the HTML can be pasted without editing.

## Hard bans
Keyword stuffing, padding for length, fabricated experience/prices/codes/claims/statistics, clickbait titles, copying competitors, artificial FAQ, fake bylines or invented author credentials, sacrificing user value for a Rank Math score, changing a working URL without strong reason, mass-producing near-duplicate pages (Google treats this as scaled content abuse).

## Domain adaptation
The skill is topic-agnostic. Swap in the right entities, terminology, safety rules, and source hierarchy for the domain (automotive, medical, legal, finance, home services, software, and so on) while keeping the same structure and quality rules.

## References (read when needed)
- `references/output-format.md`: deliverable order and contents
- `references/geo-guide.md`: what is and is not evidence-based for AI answer engines; measuring AI visibility
- `references/schema-guide.md`: schema types worth adding, JSON-LD templates, deprecation timeline
- `references/eeat-and-sources.md`: Who/How/Why, AI disclosure, source hierarchy, claim labels, YMYL
- `references/persian-writing.md`: Persian typography, ZWNJ, digits, tone, cliché list
- `references/search-console-analysis.md`: reading a Search Console export, query-to-section mapping
- `references/correction-patterns.md`: Mode B diagnosis patterns and extra output section
- `references/rank-math-templates.md`: Rank Math fields, title/meta formulas, length guidance
- `references/checklists.md`: research, quality, structure, and final-delivery checklists
- `references/examples.md`: before/after examples (direct answer, title/meta, tone)

## Scripts
- `scripts/analyze_gsc.py`: turn a Search Console CSV export into ranked opportunities (stdlib only)
- `scripts/lint_article.py`: structural and Persian-typography checks on article HTML (stdlib only)
