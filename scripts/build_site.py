"""Build the voice-first journal homepage and static article site."""
from __future__ import annotations

from html import escape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"
SITE = ROOT / "site"
OUT = ROOT / "_site"
SKILL_ASSETS = ROOT / "skills" / "olah-style-journal" / "assets"


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key and key.startswith("journal:") and values.get("content"):
                self.meta[key.removeprefix("journal:")] = values["content"].strip()
        elif tag == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def extract_post_metadata(path: Path, posts_root: Path = POSTS) -> dict[str, str]:
    parser = MetadataParser()
    parser.feed(path.read_text(encoding="utf-8"))
    meta = parser.meta
    title = meta.get("title") or "".join(parser.title_parts).strip()
    date = meta.get("date", "")
    if not title or not date or not meta.get("summary") or not meta.get("category"):
        raise ValueError(f"Missing journal metadata in {path}")
    if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", date):
        raise ValueError(f"Invalid journal date {date!r} in {path}")
    relative_dir = path.parent.relative_to(posts_root).as_posix()
    prefix = "posts/" if posts_root.resolve() == POSTS.resolve() else ""
    tags = [item.strip() for item in meta.get("tags", "").split(",") if item.strip()]
    return {
        "title": title,
        "date": date,
        "summary": meta["summary"],
        "category": meta["category"],
        "category_label": meta.get("category-label", meta["category"]),
        "tags": ", ".join(tags),
        "cover": meta.get("cover", ""),
        "cover_alt": meta.get("cover-alt", title),
        "url": prefix + relative_dir + "/",
    }


def discover_posts(posts_root: Path = POSTS) -> list[dict[str, str]]:
    if not posts_root.exists():
        return []
    files = sorted(posts_root.glob("**/index.html"))
    posts = [extract_post_metadata(path, posts_root) for path in files]
    return sorted(posts, key=lambda item: item["date"], reverse=True)


def render_post_card(post: dict[str, str]) -> str:
    title = escape(post["title"], quote=True)
    summary = escape(post["summary"], quote=True)
    category = escape(post["category"], quote=True)
    category_label = escape(post["category_label"])
    date = escape(post["date"], quote=True)
    url = escape(post["url"], quote=True)
    search = escape(" ".join((post["title"], post["summary"], post["category_label"], post["tags"])).lower(), quote=True)
    cover = ""
    if post.get("cover"):
        cover_path = post["url"] + escape(post["cover"], quote=True)
        cover = (
            f'<div class="post-cover"><img src="{cover_path}" '
            f'alt="{escape(post.get("cover_alt", title), quote=True)}" loading="lazy"></div>'
        )
    return (
        f'<article class="post-card" data-date="{date}" data-category="{category}" data-search="{search}">'
        f'<a class="post-card-link" href="{url}">{cover}'
        f'<div class="post-card-body"><div class="post-meta"><time datetime="{date}">{date}</time>'
        f'<span class="category-label">{category_label}</span></div>'
        f'<h3>{title}</h3><p>{summary}</p>'
        f'<span class="read-more">进入这一天 <span aria-hidden="true">↗</span></span>'
        f'</div></a></article>'
    )


def render_category_options(posts: list[dict[str, str]]) -> str:
    categories: dict[str, str] = {}
    for post in posts:
        categories.setdefault(post["category"], post["category_label"])
    return "".join(
        f'<option value="{escape(slug, quote=True)}">{escape(label)}</option>'
        for slug, label in sorted(categories.items(), key=lambda pair: pair[1])
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    posts = discover_posts()
    template = (SITE / "index.html").read_text(encoding="utf-8")
    cards = "\n".join(render_post_card(post) for post in posts)
    if not cards:
        cards = '<p class="empty-state">还没有发布日志。下一次口述整理完成后，文章会出现在这里。</p>'

    replacements = {
        "{{POST_COUNT}}": str(len(posts)),
        "{{POST_CARDS}}": cards,
        "{{CATEGORY_OPTIONS}}": render_category_options(posts),
    }
    for token, value in replacements.items():
        template = template.replace(token, value)

    (OUT / "index.html").write_text(template, encoding="utf-8")
    shutil.copytree(SITE / "assets", OUT / "assets", dirs_exist_ok=True)
    if POSTS.exists():
        shutil.copytree(POSTS, OUT / "posts", dirs_exist_ok=True)

    # The public site needs only the shared CSS and interaction helper, not the full authoring docs.
    for folder in ("css", "js"):
        source = SKILL_ASSETS / folder
        if source.exists():
            shutil.copytree(source, OUT / "skills" / "olah-style-journal" / "assets" / folder, dirs_exist_ok=True)

    public_index = {"count": len(posts), "posts": posts}
    (OUT / "posts").mkdir(parents=True, exist_ok=True)
    (OUT / "posts" / "index.json").write_text(
        json.dumps(public_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built voice journal: {len(posts)} article(s) -> {OUT}")


if __name__ == "__main__":
    main()
