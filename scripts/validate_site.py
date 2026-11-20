"""Validate the generated voice journal site and its local visual assets."""
from __future__ import annotations

from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import json
import xml.etree.ElementTree as ET

from build_site import discover_posts

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
SKILL_VALIDATOR = ROOT / "skills" / "olah-style-journal" / "scripts" / "validate.py"
POSTS = ROOT / "posts"

OBSOLETE_PATHS = (
    "config/projects.json",
    "data/github_activity",
    "data/latest-activity.json",
    "data/entries.json",
    "scripts/journal_pipeline.py",
    "skills/journal-reporting",
    "reports",
)


class PageAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.h2 = 0
        self.main = 0
        self.nav = 0
        self.figures = 0
        self.figure_has_visual: list[bool] = []
        self.figure_has_caption: list[bool] = []
        self.images: list[str] = []
        self.assets: list[str] = []
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.meta: dict[str, str] = {}
        self.buttons = 0
        self.in_figure = False
        self.in_caption = False
        self.caption_text = ""

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "meta":
            key = values.get("name", "")
            if key.startswith("journal:"):
                self.meta[key.removeprefix("journal:")] = values.get("content", "")
        elif tag == "h1":
            self.h1 += 1
        elif tag == "h2":
            self.h2 += 1
        elif tag == "main":
            self.main += 1
        elif tag == "nav":
            self.nav += 1
        elif tag == "figure":
            self.figures += 1
            self.figure_has_visual.append(False)
            self.figure_has_caption.append(False)
            self.in_figure = True
        elif tag == "figcaption" and self.in_figure:
            self.in_caption = True
        elif tag == "img":
            src = values.get("src", "")
            if src:
                self.images.append(src)
            if self.in_figure and self.figure_has_visual:
                self.figure_has_visual[-1] = True
        elif tag == "svg" and self.in_figure and self.figure_has_visual:
            self.figure_has_visual[-1] = True
        elif tag in ("script", "link"):
            key = "src" if tag == "script" else "href"
            value = values.get(key, "")
            if value and not value.startswith(("https://", "http://", "data:", "#")):
                self.assets.append(value)
        elif tag == "a":
            href = values.get("href", "")
            if href:
                self.links.append(href)
        elif tag == "button":
            self.buttons += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "figure":
            self.in_figure = False
        elif tag == "figcaption":
            if self.in_figure and self.figure_has_caption:
                self.figure_has_caption[-1] = bool(self.caption_text.strip())
            self.caption_text = ""
            self.in_caption = False

    def handle_data(self, data: str) -> None:
        if self.in_caption:
            self.caption_text += data


def local_asset_exists(page: Path, asset: str) -> bool:
    if asset.startswith(("https://", "http://", "data:", "#", "mailto:")):
        return True
    return (page.parent / asset.split("#", 1)[0]).resolve().exists()


def audit_page(path: Path) -> list[str]:
    parser = PageAudit()
    parser.feed(path.read_text(encoding="utf-8"))
    failures: list[str] = []
    if parser.h1 != 1:
        failures.append(f"{path}: expected exactly one H1, found {parser.h1}")
    if parser.main < 1 or parser.nav < 1:
        failures.append(f"{path}: missing semantic main or navigable TOC")
    if parser.h2 < 3:
        failures.append(f"{path}: expected at least three explanatory sections")
    if not parser.meta.get("date") or not parser.meta.get("title") or not parser.meta.get("summary"):
        failures.append(f"{path}: missing journal date/title/summary metadata")
    if not parser.figures:
        failures.append(f"{path}: no semantic figures")
    if any(not value for value in parser.figure_has_visual):
        failures.append(f"{path}: a figure has no image or SVG")
    if any(not value for value in parser.figure_has_caption):
        failures.append(f"{path}: a figure has no explanatory figcaption")
    if parser.buttons < 2:
        failures.append(f"{path}: expected at least two meaningful interactive controls")
    for asset in parser.assets + parser.images:
        if not local_asset_exists(path, asset):
            failures.append(f"{path}: missing local asset {asset}")
    return failures


def validate_svg(path: Path) -> list[str]:
    failures: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        return [f"{path}: invalid SVG XML: {exc}"]
    if not root.attrib.get("viewBox"):
        failures.append(f"{path}: SVG missing viewBox")
    names = {node.tag.split("}")[-1] for node in root.iter()}
    if "title" not in names or "desc" not in names:
        failures.append(f"{path}: SVG must include title and desc")
    return failures


def main() -> None:
    failures: list[str] = []
    if not (OUT / "index.html").exists():
        raise SystemExit("Run python scripts/build_site.py first")

    home = (OUT / "index.html").read_text(encoding="utf-8")
    if home.count("<h1") != 1:
        failures.append("Homepage must contain exactly one H1")
    if 'id="post-grid"' not in home or 'id="search-input"' not in home:
        failures.append("Homepage is missing the journal grid or search control")

    source_posts = discover_posts()
    public_posts = sorted((OUT / "posts").glob("**/index.html"))
    if len(source_posts) != len(public_posts):
        failures.append(f"Homepage build copied {len(public_posts)} posts; expected {len(source_posts)}")

    for page in public_posts:
        failures.extend(audit_page(page))
        for svg in page.parent.glob("assets/*.svg"):
            failures.extend(validate_svg(svg))

    # Run the canonical Olah-style Skill validator against each source article.
    spec = importlib.util.spec_from_file_location("olah_journal_validator", SKILL_VALIDATOR)
    if spec is None or spec.loader is None:
        failures.append(f"Cannot load Skill validator: {SKILL_VALIDATOR}")
    else:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for source_page in sorted(POSTS.glob("**/index.html")):
            result = module.validate(source_page)
            if not result.get("pass"):
                failures.extend(f"Skill validation {source_page}: {issue}" for issue in result.get("failures", []))

    try:
        index = json.loads((OUT / "posts" / "index.json").read_text(encoding="utf-8"))
        if index.get("count") != len(source_posts):
            failures.append("posts/index.json count does not match discovered articles")
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"Invalid posts/index.json: {exc}")

    for rel in OBSOLETE_PATHS:
        if (ROOT / rel).exists():
            failures.append(f"Retired GitHub activity/reporting component still exists: {rel}")

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Validation passed: homepage + {len(public_posts)} visual article(s), local SVG/assets, no repository-activity tracking.")


if __name__ == "__main__":
    main()
