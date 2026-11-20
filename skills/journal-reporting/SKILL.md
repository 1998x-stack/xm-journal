---
name: journal-reporting
description: Turn daily conversation records into evidence-grounded daily, ISO-weekly and calendar-monthly journals with original SVG visualizations and responsive GitHub Pages reports.
---

# Journal Reporting

## Use for
Daily progress capture, journal organization, trend analysis, daily report generation, weekly/monthly synthesis and period-boundary handling.

## Principle
Daily records are evidence; weekly/monthly reports are derived analysis. Unknown is not zero. Do not infer missing activity.

## Mandatory workflow
1. Read AGENTS.md, taxonomy and existing records.
2. Collect only user-shared facts and relevant connected materials. Preserve source URL, filename and date.
3. Create/update the daily source record with summary, category, tags, workstreams, outcomes, decisions, blockers, risks, next actions and metrics.
4. Build an evidence ledger: claim, source, confidence and date range. Separate confirmed outcomes from plans/hypotheses.
5. Design a specific visualization: timeline, workstream map, progress trend, dependency graph or category distribution. Use SVG title/desc and accessible fallback.
6. Evaluate triggers in Asia/Shanghai: ISO week Monday–Sunday; calendar month first–last day.
7. After Sunday finalization generate daily + weekly. After month-end finalization generate daily + monthly. If both apply, generate all three.
8. Aggregate only entries in the exact period. Show missing dates and link every claim to source entries.
9. Update report catalog and homepage. Run tests, build, validation and browser checks.
10. Report changed files and deployment status honestly.

## Report structure
- Exact period, generated time, coverage and completeness.
- 3–5 evidence-backed executive conclusions.
- KPI strip: completed items, active workstreams, decisions, blockers, captured days. Unknown = 未记录.
- Timeline and gaps.
- Workstream outcomes with evidence and status.
- Decisions and rationale.
- Risks, blockers and dependencies.
- Lessons and patterns.
- Prioritized next-period actions; owners only when known.
- Visual appendix with definitions.

## Aggregation
Deduplicate repeated mentions while preserving distinct outcomes. Separate activity volume from impact. Compare only comparable periods. Keep unresolved work as carry-over. Record source_entry_ids and SHA-256 source_hashes. Final report only when all expected dates are checked; otherwise label interim.

## HTML and verification
Semantic, responsive, print-friendly and accessible; one H1, valid heading order, no remote dependencies, keyboard-operable controls, reduced-motion support. Validate Sunday, month-end, leap day, year rollover, simultaneous boundaries, incomplete periods and backfills. Browser QA desktop/tablet/360/390px. Skipped checks are NOT VERIFIED.
