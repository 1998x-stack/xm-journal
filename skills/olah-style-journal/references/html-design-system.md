# HTML / CSS design contract for journal articles

An article is a readable visual essay, not a corporate dashboard or slide deck. Use generous whitespace, a narrow reading column, visible navigation and diagrams that explain one idea at a time.

## Semantic HTML

- One h1 per page.
- Use main, article, nav, header, section, figure and figcaption according to meaning.
- Use a skip link, descriptive link text and keyboard-visible focus.
- Every SVG has viewBox, title, desc and unique IDs.
- Every non-decorative image has useful alt text.
- Every interactive control is a native button or input with an accessible name.

## Reading layout

| Token | Default | Purpose |
|---|---|---|
| Body | 17px / 1.85 | Comfortable Chinese long-form reading |
| Article width | 760–820px | Keep paragraphs and figures legible |
| Sidebar | 190–220px | Desktop section navigation |
| Main section gap | 3.5–4.25rem | Progressive narrative rhythm |
| Paper | warm off-white | Reduce the feel of an admin dashboard |
| Ink | dark green-grey | High-contrast reading |
| Accent | restrained green / orange / violet | Consistent visual semantics |

## Responsive behavior

- At <=900px, move the TOC above the article.
- At <=480px, keep at least 16px side padding and readable figure labels.
- At 360px and 390px, the document must not overflow horizontally.
- Wide diagrams may scroll only inside an explicitly labeled, keyboard-focusable region.
- Respect prefers-reduced-motion.
- Print mode hides navigation and interaction controls but preserves the full explanation and figures.

## Interaction

- Static content must explain the main point before JavaScript runs.
- Controls must be keyboard-operable and expose selected state.
- Do not autoplay, flash, or use decorative controls.
- No analytics, trackers, CDN scripts, or remote fonts.
- A no-JavaScript reader must still understand the article.

## Homepage

The homepage is an editorial index of daily visual entries:
- newest entries first;
- a unique cover or diagram per entry;
- readable title, date, category and short summary;
- client-side search and category filtering as progressive enhancement;
- no Commit/PR/CI metrics, project cards or repository activity charts.
