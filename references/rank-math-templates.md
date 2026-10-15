# Rank Math & SEO Package Templates

Rank Math's test list is advisory. If a test conflicts with reader value, reader value wins, and the deviation goes into the final check. The user should confirm the package in the Rank Math panel, since interfaces change between versions.

## Fields to deliver

- **Focus Keyword:** one primary phrase in the form users actually type (check ZWNJ/spelling variants, see `persian-writing.md`)
- **Secondary Keywords:** 2–4 genuinely related phrases, not synonyms for the sake of count
- **SEO Title:** about 50–60 characters is a safe upper rule of thumb; a complete natural title that is shorter (even 40–45) is fine, so do not pad it. Google truncates by pixel width, not character count, and often rewrites titles, so lead with the key phrase and keep a concrete benefit
- **Meta Description:** about 120–155 characters: problem + promise + soft CTA only if natural. Google often shows a different snippet; the meta still sets the default and affects clicks
- **URL Slug:** short, stable, readable, consistent with the site (Persian or Latin); never change a working URL without a redirect plan
- **Schema:** see `schema-guide.md`. Default `Article`/`BlogPosting` + `BreadcrumbList`; add `LocalBusiness` only for real local service pages. FAQ markup optional
- **Canonical:** usually self-referencing; list any exception
- **Breadcrumb:** suggested path
- **Social Title / Social Description / social image:** short and honest, consistent with the page
- **Image ALT** for every proposed image: describe what is shown, naturally, no keyword stuffing
- **Internal links:** URL + suggested natural anchor + where it goes
- **External links:** URL + reason (authority source); mark `nofollow`/`sponsored` where appropriate
- **FAQ:** only if real Q&A is on the page (see `checklists.md`)

## Title formula examples (adapt to language and intent)

- [Problem] در [Model/Context] — علت‌ها، علائم و راه‌حل
- معنی [Error Message] روی نمایشگر [Brand/Model]
- تعمیر [Part/System] [Brand/Model] — هزینه، زمان و نکات مهم
- [Service] در [City] — راهنمای کامل + مراجعه

Never force the exact keyword if it makes the title unnatural. Do not use "ultimate guide" or numbers the page does not deliver. Title and H1 should align in meaning but need not be identical strings.

## Meta description principles

1. Restate the core problem in the user's language
2. Promise concrete value (causes, diagnosis steps, when to visit)
3. Soft CTA only if it fits («برای بررسی دقیق‌تر با تعمیرگاه تخصصی تماس بگیرید»)
4. No keyword repetition
5. Match the dominant search intent

## Rank Math tests: common conflicts and how to decide

| Test | When to bend it |
|---|---|
| Keyword in the first 10% of content | Satisfy only if a natural first sentence allows; never distort the opening |
| Keyword in an H2/H3 | One natural use is enough; do not repeat across headings |
| Keyword density | Ignore the target if reaching it needs repetition; check the linter for runaway repetition instead |
| Content length | Length follows the questions to answer; do not pad |
| Short paragraphs / table of contents | Keep, they help readers |
| External link tests | Add only authoritative links that support a claim |

## Pre-publish checks for the user
- Rich Results Test / Schema Markup Validator on the live URL
- Page source: one H1, one set of Article schema (no duplicates from a theme plus Rank Math)
- Mobile view reads cleanly; images have ALT and sensible file size
- URL Inspection → request indexing after publishing or major changes
