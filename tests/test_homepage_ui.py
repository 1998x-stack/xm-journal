"""Browser checks for homepage date filtering and seven-day pagination."""
from pathlib import Path
import shutil

import pytest
from playwright.sync_api import sync_playwright

from scripts.build_site import SITE, render_post_card, render_category_options


ENTRIES = [
    ("2026-11-23", "reflection"),
    ("2026-11-21", "learning"),
    ("2026-11-17", "reflection"),
    ("2026-11-16", "work"),
    ("2026-11-10", "learning"),
    ("2026-11-09", "reflection"),
    ("2026-11-03", "reflection"),
    ("2026-10-30", "work"),
]


def create_homepage(tmp_path: Path) -> Path:
    """Use the actual template and assets, but a deliberately sparse calendar."""
    posts = [
        {
            "date": date,
            "title": f"日志 {date}",
            "summary": f"{date} 的日常记录",
            "category": category,
            "category_label": {"reflection": "复盘与思考", "learning": "学习与成长",
                               "work": "工作与协作"}[category],
            "tags": category,
            "url": f"posts/{date}/",
            "cover": "",
            "cover_alt": "",
        }
        for date, category in ENTRIES
    ]
    source = (SITE / "index.html").read_text(encoding="utf-8")
    html = (source.replace("{{POST_COUNT}}", str(len(posts)))
                   .replace("{{CATEGORY_OPTIONS}}", render_category_options(posts))
                   .replace("{{POST_CARDS}}", "\n".join(map(render_post_card, posts))))
    page_file = tmp_path / "index.html"
    page_file.write_text(html, encoding="utf-8")
    assets = tmp_path / "assets"
    assets.mkdir()
    shutil.copy2(SITE / "assets/app.js", assets / "app.js")
    shutil.copy2(SITE / "assets/style.css", assets / "style.css")
    return page_file


@pytest.fixture
def homepage(tmp_path: Path):
    page_file = create_homepage(tmp_path)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--no-sandbox"])
        yield browser, page_file
        browser.close()


def visible_dates(page):
    return page.locator(".post-card:visible time").all_text_contents()


def test_default_newest_first_and_seven_calendar_day_windows(homepage):
    browser, path = homepage
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(path.as_uri())

    assert visible_dates(page) == ["2026-11-23", "2026-11-21", "2026-11-17"]
    assert page.locator("#page-range").inner_text() == "2026.11.17 — 2026.11.23（7 天）"
    assert page.locator("#page-indicator").inner_text() == "第 1 / 4 页"
    assert page.locator("#page-newer").is_disabled()
    assert page.locator("#post-count").inner_text() == "8"

    page.locator("#page-older").click()
    assert visible_dates(page) == ["2026-11-16", "2026-11-10"]
    assert page.locator("#page-range").inner_text() == "2026.11.10 — 2026.11.16（7 天）"
    page.locator("#page-older").click()
    assert visible_dates(page) == ["2026-11-09", "2026-11-03"]
    page.locator("#page-older").click()
    assert visible_dates(page) == ["2026-10-30"]
    assert page.locator("#page-older").is_disabled()
    page.locator("#page-newer").click()
    assert visible_dates(page) == ["2026-11-09", "2026-11-03"]
    assert not errors
    page.close()


def test_filters_combine_and_reset_pagination(homepage):
    browser, path = homepage
    page = browser.new_page()
    page.goto(path.as_uri())

    page.locator("#category-filter").select_option("learning")
    assert visible_dates(page) == ["2026-11-21"]
    assert page.locator("#page-indicator").inner_text() == "第 1 / 2 页"
    page.locator("#page-older").click()
    assert visible_dates(page) == ["2026-11-10"]

    # New filters reset to the first page, with inclusive date boundaries.
    page.locator("#date-from").fill("2026-11-10")
    page.locator("#date-from").dispatch_event("change")
    page.locator("#date-to").fill("2026-11-21")
    page.locator("#date-to").dispatch_event("change")
    assert visible_dates(page) == ["2026-11-21"]
    page.locator("#search-input").fill("2026-11-10")
    assert visible_dates(page) == ["2026-11-10"]
    assert page.locator("#page-indicator").inner_text() == "第 1 / 1 页"
    assert page.locator("#post-count").inner_text() == "8"

    page.locator("#date-from").fill("2026-11-22")
    page.locator("#date-from").dispatch_event("change")
    assert page.locator(".post-card:visible").count() == 0
    assert "开始日期不能晚于结束日期" in page.locator("#empty-state").inner_text()

    page.locator("#reset-filters").click()
    assert visible_dates(page) == ["2026-11-23", "2026-11-21", "2026-11-17"]
    assert page.locator("#category-filter").input_value() == ""
    assert page.locator("#date-from").input_value() == ""
    assert page.locator("#date-to").input_value() == ""
    page.close()


def test_sparse_week_and_responsive_layout(homepage):
    browser, path = homepage
    for width, height in [(1440, 900), (768, 1024), (390, 844), (360, 800)]:
        page = browser.new_page(viewport={"width": width, "height": height})
        page.goto(path.as_uri())
        assert page.locator("h1").count() == 1
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
        assert page.locator("#pagination").is_visible()
        assert visible_dates(page) == ["2026-11-23", "2026-11-21", "2026-11-17"]
        page.close()

    # When the latest and oldest entries are far apart, an empty seven-day
    # window is shown explicitly rather than hiding it or changing window size.
    page = browser.new_page()
    page.goto(path.as_uri())
    page.locator("#category-filter").select_option("work")
    assert visible_dates(page) == ["2026-11-16"]
    page.locator("#page-older").click()
    assert visible_dates(page) == []
    assert "这七天还没有日志" in page.locator("#empty-state").inner_text()
    page.locator("#page-older").click()
    assert visible_dates(page) == ["2026-10-30"]
    page.close()

    # The unenhanced static HTML remains a complete chronological index.
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(path.as_uri())
    assert visible_dates(page) == [date for date, _ in ENTRIES]
    context.close()
