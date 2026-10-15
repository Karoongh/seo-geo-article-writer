# Schema Guide (dated: October 2026)

Structured data is for eligibility in rich results and for helping systems understand the page. Google says no special schema is needed for AI features. Rule that never changes: markup must match what is visible on the page, with real values.

## Google deprecation timeline (what changed)
Source summary: Patrick Stox's schema deprecation timeline, cross-checked against Google Search Central notices.

- Aug 2023: FAQ rich results limited to well-known government and health sites.
- Sep 14, 2023: HowTo rich results removed on desktop and mobile.
- 2024–2025: Sitelinks searchbox, Special Announcement, Book Actions (partial), Course Info, Claim Review, Estimated Salary, Learning Video, Vehicle Listing, Practice Problem retired from rich results/tooling.
- May 7, 2026: FAQ rich results removed entirely, including government and health sites.
- Jun 2026: FAQ reporting and Rich Results Test support dropped; FAQPage documentation removed Jun 15, 2026.
- Google states these types stay valid schema.org vocabulary and are still parsed "for understanding"; only the visible rich result is gone. Google says removals do not change ranking.

Consequence for this skill: never present FAQPage or HowTo as a way to get rich results or more clicks. FAQ content on the page is still good for readers; FAQPage JSON-LD is optional and harmless when it mirrors the visible Q&A.

## What to recommend by page type

| Page type | Recommended markup | Notes |
|---|---|---|
| Blog / guide / explainer | `Article` or `BlogPosting` + `BreadcrumbList` | Real `author` (Person with a profile URL), `datePublished`, `dateModified`, `image`, `publisher`. |
| Local service page | `LocalBusiness` (or a specific subtype) + `Article`/`WebPage` | Only real NAP (name, address, phone), hours, geo. Match Google Business Profile. |
| Site-wide | `Organization` + `WebSite` | `WebSite` still drives site name. |
| Product / review | `Product` + `Review`/`AggregateRating` only with genuine, visible reviews | Fake or self-written reviews violate policy. |
| Video on page | `VideoObject` | Only if a video is really embedded. |
| FAQ on page | `FAQPage` optional | No rich result; keep only if it matches the visible text. |
| Step-by-step | none required; use a numbered list | `HowTo` gives no rich result. |

Check current support in Google's Search Gallery before promising any rich result, since this list changes.

## Rank Math notes
- Rank Math's schema generator can output Article/BlogPosting, Local Business, Product and others from its Schema tab, and its FAQ block adds FAQ schema (as far as I know; confirm in the user's plugin version). That is harmless, see above.
- Rank Math's "SEO score" and test list are advisory. Where a test conflicts with reader value (for example keyword in the first 10% of the text, a forced H2 keyword), reader value wins; mention the deliberate deviation in the final check.
- Always have the user validate with the Rich Results Test or the Schema Markup Validator after publishing; the validator, not the plugin, is the final word.

## JSON-LD templates (replace every placeholder with real data; delete fields you cannot fill)

### Article / BlogPosting
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "mainEntityOfPage": {"@type": "WebPage", "@id": "https://example.com/slug/"},
  "headline": "ARTICLE H1 (max ~110 chars)",
  "description": "Meta-description-style summary",
  "image": ["https://example.com/images/main.jpg"],
  "datePublished": "2026-10-16T09:00:00+03:30",
  "dateModified": "2026-10-16T09:00:00+03:30",
  "inLanguage": "fa-IR",
  "author": {"@type": "Person", "name": "REAL AUTHOR", "url": "https://example.com/author/name/"},
  "publisher": {"@type": "Organization", "name": "BRAND", "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}}
}
```

### BreadcrumbList
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "خانه", "item": "https://example.com/"},
    {"@type": "ListItem", "position": 2, "name": "دسته", "item": "https://example.com/category/"},
    {"@type": "ListItem", "position": 3, "name": "عنوان مقاله"}
  ]
}
```

### LocalBusiness (only with real details)
```json
{
  "@context": "https://schema.org",
  "@type": "AutoRepair",
  "name": "BUSINESS NAME",
  "url": "https://example.com/",
  "telephone": "+98-...",
  "address": {"@type": "PostalAddress", "streetAddress": "...", "addressLocality": "...", "addressCountry": "IR"},
  "openingHours": "Sa-Th 08:00-18:00"
}
```
Pick the most specific schema.org subtype that is true (for example `AutoRepair`, `Dentist`, `Plumber`); use `LocalBusiness` if none fits.

### FAQPage (optional; mirror visible text exactly)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Visible question text",
    "acceptedAnswer": {"@type": "Answer", "text": "Visible answer text"}
  }]
}
```

## Common errors to check
- Author is a brand name pretending to be a person, or an invented expert.
- `dateModified` bumped without real changes.
- Prices, ratings, hours, or phone numbers in schema that differ from the page.
- Two plugins both outputting Article schema (duplicate entities). Ask the user to check the page source.
- Image URLs that 404 or are blocked by robots.txt.

## Sources to re-verify (read October 2026)
- Schema and rich result deprecations timeline (Patrick Stox), https://patrickstox.com/technical-seo/on-page/structured-data/schema-deprecations/ (page updated July 2026; the August 2026 FAQ Search Console API change was unconfirmed there)
- Google Search Gallery for current rich result support: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- Google's FAQ and HowTo documentation changes are announced on the Search Central blog; check it before promising any rich result.
