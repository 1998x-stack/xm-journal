# Architecture

## Source of truth
- journal/daily/YYYY/MM/YYYY-MM-DD.md: human-readable daily records.
- data/entries.json: normalized site index.
- data/taxonomy.json: category and tag registry.
- reports/daily/, reports/weekly/, reports/monthly/: generated visual reports.
- reports/index.json: report catalog and source hashes.

Daily notes are authoritative. Reports and pages are reproducible views; never hand-edit generated HTML.

## Pipeline
Capture → normalize → classify → evidence ledger → visualize → roll up → build → validate → browser QA → deploy.

Daily finalization updates the day report and indexes. Weekly/monthly aggregation reads only finalized entries. Boundary dates can generate daily + weekly + monthly outputs in one run.

## Idempotency
Each entry has a stable date/slug ID. Reports record source IDs and SHA-256 hashes. Backfills invalidate every containing weekly/monthly report. Missing days remain visible gaps.

## Publishing
Static, offline-first GitHub Pages. No server/database required. Search and charts use generated local JSON and native SVG. Pages must remain readable without JavaScript.
