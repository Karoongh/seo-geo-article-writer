# GEO Guide: What Is Evidence-Based and What Is Not

GEO (generative engine optimization) is a young field full of confident advice with little evidence. This file separates what is documented from what is plausible folklore, so the skill does not sell certainty it does not have. Verify the status of anything here that matters, since this area moves fast (last checked October 2026).

## What Google officially says (primary source)
Source: Google Search Central, "Optimizing your website for generative AI features on Google Search" and "AI features and your website" (developers.google.com/search/docs).

- Optimizing for AI Overviews and AI Mode is "still SEO". The features rest on core ranking and quality systems.
- Eligibility: the page must be indexed and eligible to show in Search with a snippet. There are no additional requirements.
- Google says you do not need: llms.txt or other AI-specific files, special schema.org markup, content "chunking", rewriting content in a special style for AI, or hunting for inauthentic mentions. Mass-producing pages to manipulate AI responses violates the scaled content abuse policy.
- Google does recommend: non-commodity, people-first content with a unique viewpoint; clear paragraphs, sections and headings; crawlable pages (check robots.txt and CDN); internal links; good page experience; important content in text form; supporting images and video where they fit; structured data that matches visible text; current Merchant Center and Business Profile data for local/commercial sites; semantic HTML where practical.
- Controls: `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`; Google-Extended for training/grounding in other Google systems.
- Measurement: AI Overviews and AI Mode traffic is counted inside the normal Search Console "Web" performance data; Search Console also has a generative AI performance report. Treat third-party tools that claim to see Google's internal AI metrics with suspicion.

## Other engines (ChatGPT, Perplexity, Gemini app, Copilot)
Google's guidance covers Google only. Other engines "may weight signals differently" and they publish little. Practical stance:
- Plausible and low-cost: be crawlable (do not block their search crawlers in robots.txt if you want visibility; check each vendor's current crawler documentation), be factually clear, quote and name sources, keep entities consistent (brand, address, author), have pages that load as plain text.
- Unproven: that llms.txt, FAQ schema, specific word counts, or "citation-bait" formats raise citation rates. Studies exist but are vendor-run or small and conflict. Do not state them as fact; if the user asks, say they are unverified.
- Never promise "this will get you cited by ChatGPT". Say what you did and what it can plausibly help with.

## Writing for extraction without writing for machines
The one tactic that costs nothing and helps humans too: the standalone answer.
- Put a 1–3 sentence answer directly under the heading that asks the question. It must name its subject (no "this", "it" with the referent two paragraphs earlier) and make sense if quoted alone.
- Then add the nuance, conditions, and exceptions. Do not trade correctness for brevity: a wrong clean sentence is worse than a hedged right one. Include the qualifier inside the sentence ("معمولاً"، "در بیشتر خودروهای X"، "اگر چراغ چشمک می‌زند").
- Make claims attributable: name the source or standard in the sentence when a fact is not common knowledge.
- Use a table for genuine comparisons and lookups; use a numbered list for real sequences. Avoid decorative structure.
- Keep entity names consistent (same spelling of brand, model, service, place) and spell out abbreviations once.
- Do not split content into artificially tiny pages or sections to be "chunk-friendly"; Google says this is not required.

## What makes content hard for AI to ignore (and for Google to rank)
- Information gain: something the top results lack (original data supplied by the user, a clearer diagnostic order, a correction, an honest comparison).
- Verifiable specifics with sources, instead of generic advice any model could produce.
- A real, named author or business with a visible reason to know the topic (see `eeat-and-sources.md`).
- Freshness only when the topic changes; add a visible "last reviewed" date only if someone actually reviewed it.

## Measuring (what to tell the user)
1. Search Console Performance → Web: watch impressions, clicks, CTR, position per query/page after changes (allow weeks; Google recrawl takes days to months).
2. Search Console generative AI performance report where available.
3. Spot checks: ask the target questions in several engines, note whether and how the brand/page appears. Record date and exact prompt; results vary run to run, so a single check proves nothing.
4. Analytics: conversions and engagement, not only traffic. Google reports AI-feature clicks tend to be higher quality, but verify on the user's own data.

## Red flags in third-party GEO advice
Guaranteed citations; "secret" formats; paid "AI visibility scores" presented as Google data; instructions to create many near-duplicate pages; fake reviews/mentions; hidden text for LLMs. Decline these and say why.

## Sources to re-verify (read October 2026)
- Google Search Central: Optimizing your website for generative AI features on Google Search, https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google Search Central: AI features and your website, https://developers.google.com/search/docs/appearance/ai-features
- Search Engine Journal coverage (May 15, 2026), https://www.searchenginejournal.com/googles-new-ai-search-guide-calls-aeo-and-geo-still-seo/575026/
- Google Search Central: Creating helpful, reliable, people-first content, https://developers.google.com/search/docs/fundamentals/creating-helpful-content
