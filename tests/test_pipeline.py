import datetime as dt
from scripts.journal_pipeline import day_bounds, frontmatter, report_content

def test_frontmatter_parses_metadata_and_body():
    meta, body = frontmatter("---\ndate: 2026-11-20\ntags: [agents, ci-cd]\nsummary: \"hello\"\n---\n# Today")
    assert meta["date"] == "2026-11-20"
    assert meta["tags"] == ["agents", "ci-cd"]
    assert body == "# Today"

def test_local_day_bounds_are_24_hours_and_utc_encoded():
    start, end = day_bounds(dt.date(2026, 11, 20))
    assert start.endswith("Z") and end.endswith("Z")
    assert dt.datetime.fromisoformat(end.replace("Z","+00:00")) - dt.datetime.fromisoformat(start.replace("Z","+00:00")) == dt.timedelta(days=1)

def test_weekly_rollup_counts_only_real_github_snapshots():
    day=dt.date(2026,11,20); key=day.isoformat()
    snapshots={key:{"date":key,"repositories":[]}, "2026-11-19":{"date":"2026-11-19","repositories":[]}}
    notes={"2026-11-18":{"id":"2026-11-18","title":"note","summary":"body","source_path":"journal/daily/2026/11/2026-11-18.md","body":"notes"}}
    days=[dt.date(2026,11,17)+dt.timedelta(days=i) for i in range(6)]
    html=report_content(days,snapshots,notes,dt.date(2026,11,16),dt.date(2026,11,22),"weekly")
    assert "GitHub 快照覆盖 2/7 天" in html
    assert "缺少 GitHub 快照的日期" in html

def test_leap_day_exists():
    assert dt.date(2028,2,28)+dt.timedelta(days=1) == dt.date(2028,2,29)
