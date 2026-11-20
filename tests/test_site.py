from pathlib import Path

from scripts.build_site import discover_posts, extract_post_metadata, render_post_card


def test_extract_journal_metadata(tmp_path: Path):
    article = tmp_path / "2026-11-20" / "index.html"
    article.parent.mkdir()
    article.write_text(
        '<html><head><title>Daily note</title>'
        '<meta name="journal:date" content="2026-11-20">'
        '<meta name="journal:title" content="今天的思考">'
        '<meta name="journal:summary" content="从口述到理解">'
        '<meta name="journal:category" content="reflection">'
        '<meta name="journal:category-label" content="复盘与思考">'
        '</head></html>',
        encoding="utf-8",
    )
    meta = extract_post_metadata(article, tmp_path)
    assert meta["date"] == "2026-11-20"
    assert meta["title"] == "今天的思考"
    assert meta["category"] == "reflection"


def test_discover_posts_sorts_newest_first(tmp_path: Path):
    for day in ("2026-11-19", "2026-11-20"):
        article = tmp_path / day / "index.html"
        article.parent.mkdir()
        article.write_text(
            f'<title>{day}</title><meta name="journal:date" content="{day}">'
            f'<meta name="journal:title" content="{day}">'
            '<meta name="journal:summary" content="summary">'
            '<meta name="journal:category" content="reflection">',
            encoding="utf-8",
        )
    posts = discover_posts(tmp_path)
    assert [post["date"] for post in posts] == ["2026-11-20", "2026-11-19"]


def test_post_card_escapes_untrusted_metadata():
    post = {
        "title": '<script>alert("x")</script>',
        "date": "2026-11-20",
        "summary": "A & B",
        "category": "reflection",
        "category_label": "复盘与思考",
        "tags": "ai, reflection",
        "url": "posts/2026/11/2026-11-20/",
        "cover": "",
        "cover_alt": "",
    }
    card = render_post_card(post)
    assert "<script>" not in card
    assert "&lt;script&gt;" in card
    assert "A &amp; B" in card
