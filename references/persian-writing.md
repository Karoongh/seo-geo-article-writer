# Persian Writing and Typography for Web Articles

These are editorial conventions, not Google rules. They exist because sloppy Persian reads as machine-made or careless, and because inconsistent characters split how people search for and see the same word.

## Characters
- Use Persian ی (U+06CC) and ک (U+06A9), never Arabic ي (U+064A) or ك (U+0643). Mixed forms come from copy-paste and some keyboards. `scripts/lint_article.py` flags them.
- Choose one digit style per page. Persian digits (۰۱۲۳) for running text are the usual choice in articles; Latin digits are fine for model numbers, codes, versions, units, prices in tables, and URLs. Do not mix styles inside one number. Keep error codes, part numbers and dashboard text exactly as printed (Latin).
- Use the Persian comma «،», semicolon «؛», question mark «؟», and guillemets «» or plain quotes consistently.

## نیم‌فاصله (ZWNJ, U+200C)
Use it in: the prefixes «می‌» and «نمی‌» before verbs (می‌کنم، نمی‌شود)؛ the plural endings «ها» and «های» after words that end in a joining letter (ماشین‌ها، چراغ‌های)؛ the ezafe «ی» after a final «ه» when you want it visibly separate (خانه‌ی)؛ and compounds such as دست‌کم، خوش‌حال، به‌روزرسانی.
Common slips: «می کنم» (space instead of ZWNJ), «ماشین ها» (space before plural ها), and ZWNJ wrongly inserted inside ordinary words such as «بهترین». Prefer «به‌طور» or «به طور» consistently; «بطور» is not preferred. Do not put ZWNJ inside URL slugs or in the focus keyword if users type it with a space; check how people actually type the phrase (search suggestions) and match the dominant form in the keyword while keeping the body text correct. In HTML output keep ZWNJ as the real character, not a placeholder.

## Mixed Persian/Latin
- Keep Latin terms users see on screens (OBD, ABS, ECU, Check Engine) in Latin letters, and add the Persian explanation next to the first use.
- Put a space between Persian words and adjacent Latin words; avoid placing punctuation so that bidi reordering flips it. Test RTL/LTR mixing in the HTML (`dir="rtl"` on the article container; wrap isolated LTR strings such as codes in `<bdi>` or `<span dir="ltr">`).
- Write units and symbols in a stable order: «۱۲ ولت»، «۳٫۵ لیتر» (Persian decimal separator ٫) or «3.5 لیتر» consistently.

## Tone
- Spoken-written middle register: clear like an experienced professional talking to a customer, not like a ministry circular and not slangy.
- Vary sentence length. A long sentence with a condition, then a short one with the verdict.
- Prefer concrete verbs («چک کنید»، «جدا کنید») over nominal heaps («انجام عملیات بررسی»).
- Explain jargon once, in parentheses or the next clause.
- Address the reader as «شما» consistently.

## Phrases to avoid (AI-sounding or padded openers and fillers)
- «در دنیای امروز…»، «امروزه…»، «در این مقاله قصد داریم…»، «همان‌طور که می‌دانید…»
- «بدون شک»، «بی‌تردید»، «یکی از مهم‌ترین…» when nothing is being compared
- «در پایان باید گفت…»، «نتیجه‌گیری: به طور خلاصه…» repeated summary paragraphs
- «بهترین»، «تضمینی»، «۱۰۰٪» claims about the business without proof
- Triple adjective stacks («سریع، دقیق و حرفه‌ای») used as filler
- Repeating the focus keyword in every sentence or in consecutive headings
Banned openers are checked by the linter; extend the list in the script as the user flags more.

## Keyword forms
Persian queries come in variants: with/without ZWNJ, Arabic vs Persian letters, colloquial vs formal («ماشین» vs «خودرو»)، Latin vs Persian transliteration of brands. During research list the variants users actually type (search suggestions, "related searches", Search Console queries) and cover the dominant ones naturally in headings and body, without repeating them mechanically. Search Console queries should be normalized before analysis; `scripts/analyze_gsc.py` does this.

## Choosing the focus keyword form
Pick the form people actually type, in this order of evidence: Search Console queries, Google autocomplete / related searches, then judgment. Example of a real dilemma: «ABS» (Latin) versus «ای‌بی‌اس» (Persian transliteration). If the evidence is unavailable, use the form shown on dashboards or product labels as the focus keyword (here Latin «ABS») and use the other form once, early and naturally, in the intro or an H2, so both are covered. Never repeat variants mechanically to "cover" them.

## URL slugs
Match what the site already does. If the site uses Latin slugs, transliterate consistently and keep them short; if Persian slugs, avoid ZWNJ and punctuation. Never change an existing working slug without a redirect plan.
