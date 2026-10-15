# Mode B — Correction Patterns for Published Articles

Start with the data (`search-console-analysis.md`, `scripts/analyze_gsc.py`), then match the pattern. Change the least that fixes the diagnosed problem: a page that already ranks can lose position if it is rewritten wholesale, so prefer targeted edits unless the page is thin or off-intent.

## Decision order
1. Is the page indexed and eligible for a snippet? (URL Inspection; noindex, canonical, robots.) If not, content work is premature.
2. Did anything change in the SERP for the main queries (AI Overview, new features, a stronger competitor)? Check before blaming the page.
3. Is the intent right? A page serving the wrong intent needs reframing or a different page, not tweaks.
4. Is the snippet weak (title/meta/H1)? Fix first; cheapest and most reversible.
5. Are there missing sections for high-impression query clusters? Add them.
6. Is depth, trust, or tone the issue? Rewrite those parts.

## Common failure modes and fixes

### 1. High impressions, very low CTR
**Likely causes:** title or meta does not match query wording; generic title; snippet does not answer the micro-intent; SERP feature or AI Overview absorbing clicks.
**Actions:** rewrite title and meta using phrases from the top impression queries; align H1 with the dominant query language; put a concrete promise in the first ~120 characters of meta. Re-measure after 3–4 weeks.

### 2. Ranks for many related queries, thin content
**Actions:** add a dedicated H2/H3 per high-impression related query, each starting with a short standalone answer; expand entity coverage; add a comparison or diagnostic table if it speeds understanding.

### 3. Position 5–15, stagnant clicks
**Actions:** add information the top results lack; strengthen sourcing and the distinction between certain and probable; improve internal links to and from the page; add a practical table or checklist; keep sections quotable on their own.

### 4. Artificial or AI-sounding tone
**Actions:** rewrite the intro problem-first; break long uniform paragraphs; replace formal filler with practitioner language; remove "we always…" claims the business did not supply; run the linter's cliché check.

### 5. Missing local / conversion layer
**Actions:** add a natural CTA after the most valuable section and at the end; real phone/WhatsApp/address/map only in CTA zones; link to related service pages with natural anchors.

### 6. Safety or technical risk
**Actions:** insert warnings where continuing is dangerous; soften oversimplified repair instructions; emphasize professional diagnosis where remote certainty is impossible.

### 7. Outdated content
**Actions:** verify every time-sensitive fact against current sources; update or remove stale numbers; change `dateModified` only for real changes; add a visible review date only if someone reviewed it.

### 8. Keyword cannibalization (two pages compete for one query)
**Actions:** decide which page owns the query; sharpen the other page's intent; link from the weaker to the stronger with a natural anchor; merge with a 301 only if both are thin and the user agrees.

### 9. Over-optimized page
Symptoms: keyword in every heading, repeated phrases, bold keywords, FAQ restating H2s.
**Actions:** remove repetition and artificial FAQ; keep one natural use per heading level; restore reader flow.

## Correction output extra section

When in Mode B, always add inside بخش ۱:

**تشخیص مقاله موجود:**
- Summary of current ranking queries (top by impressions with position and CTR)
- Main CTR / position problems, and which were verified in the live SERP
- Content gaps vs. high-impression query clusters
- Tone, trust, and structure issues
- Safety/accuracy issues found
- Recommended priority fixes (title/meta first, then missing sections, then depth/trust/tone)
- What the data cannot show

Also state what you deliberately left unchanged (for example a working URL or a section that already ranks) so the user does not re-break it.
