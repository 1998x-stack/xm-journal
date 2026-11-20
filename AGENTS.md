# AGENTS.md — xm-journal operating contract

## Mission
Maintain a trustworthy, searchable, visual record of research, engineering, learning, decisions and outcomes. Daily entries are the source of truth; weekly and monthly reports are derived synthesis, never replacements for daily evidence.

## Editorial standard
Write in clear Chinese by default and preserve technical English names. Explain context before conclusions. Distinguish facts, estimates, hypotheses, decisions and open questions. Never fabricate metrics, dates, outcomes, effort or causal impact.

## Taxonomy
Use exactly one primary category per entry: research, engineering, learning, product, operations, collaboration or reflection. Use controlled tags for cross-cutting themes. See docs/taxonomy.md. Keep public slugs stable.

## Daily workflow
1. Inspect existing records and relevant connected/user-provided sources.
2. Normalize the day into journal/daily/YYYY/MM/YYYY-MM-DD.md.
3. Preserve source links and evidence; deduplicate without erasing meaningful context.
4. Extract outcomes, workstreams, decisions, blockers, risks, metrics and next actions.
5. Create original SVG only when it clarifies a trend, relationship, workflow or result.
6. Update indexes and validate dates, metadata, links, charts and accessibility.
7. Never silently overwrite history; document corrections and provenance.

## Weekly / monthly roll-up
- Week = ISO Monday–Sunday. Generate after Sunday's daily entry is finalized.
- Month = calendar month in Asia/Shanghai. Generate after the month's last daily entry is finalized.
- Boundary day generates BOTH daily and applicable weekly/monthly reports. If week-end and month-end coincide, generate all three.
- Aggregate only entries inside the exact period. Link source entries and show missing-day gaps.
- Include outcomes, workstreams, evidence, decisions, metrics with denominators, risks, lessons, carry-over and next priorities.
- Compare periods only when baselines are comparable. Unknown is not zero.
- Record period_start, period_end, source_entry_ids and source_hashes. Rebuild dependent reports when a source changes.

## Visual reports
Use responsive semantic HTML, original SVG and textual explanations. Include exact period, data coverage, executive summary, KPI strip, timeline, workstream analysis, decisions, blockers, lessons and next actions. Label units, sample sizes and missing values.

## HTML / SVG
One H1, semantic landmarks, ordered headings, keyboard access, visible focus, reduced-motion and print styles. SVG needs title/description, unique IDs, legible labels and non-color-only encoding. No remote JS/fonts/trackers.

## Skills
Canonical paper skill is preserved at skills/olah-style-journal/ as migrated reference material. Journal-specific workflow is skills/journal-reporting/SKILL.md. For journal tasks, the latter and this file take precedence. Adapt the imported SVG, HTML, evidence and browser-QA practices; do not apply paper-only extraction steps to diary entries.

## Quality gates
Run python -m pytest -q, python scripts/build_site.py and python scripts/validate_site.py. Validate calendar boundaries, schema, source references, duplicate IDs, broken links, SVG parseability and mobile overflow. Missing tooling means NOT VERIFIED, not PASS.

## Publication and privacy
PR CI validates only; deploy from main via GitHub Actions. Claim Pages is live only after successful deployment and public URL verification. Store only intentionally shared information; redact credentials, tokens, identifiers and confidential third-party data.
