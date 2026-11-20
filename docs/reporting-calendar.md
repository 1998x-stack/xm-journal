# Reporting calendar

- Daily: one report per date after that day's notes are finalized.
- Weekly: ISO Monday 00:00 through Sunday 23:59:59 in Asia/Shanghai. Generate after Sunday is finalized.
- Monthly: first through last calendar day. Generate after month-end is finalized.
- Boundary dates: always generate the daily report plus every applicable roll-up. If both week and month close, generate both.
- Incomplete periods may produce clearly labelled interim previews, never final reports. List missing dates; do not invent activity.
- Backfills or corrections mark dependent reports stale and trigger deterministic regeneration.
