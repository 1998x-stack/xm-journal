#!/usr/bin/env python3
"""Static validation for a daily Olah-style journal article."""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.h2 = 0
        self.main = 0
        self.nav = 0
        self.figures = 0
        self.figure_visual: list[bool] = []
        self.figure_caption: list[bool] = []
        self.images: list[str] = []
        self.local_assets: list[str] = []
        self.anchors: list[str] = []
        self.ids: set[str] = set()
        self.metadata: dict[str, str] = {}
        self.buttons = 0
        self.in_figure = False
        self.in_caption = False
        self.caption = ""

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "meta":
            name = values.get("name", "")
            if name.startswith("journal:"):
                self.metadata[name.removeprefix("journal:")] = values.get("content", "")
        elif tag == "h1": self.h1 += 1
        elif tag == "h2": self.h2 += 1
        elif tag == "main": self.main += 1
        elif tag == "nav": self.nav += 1
        elif tag == "figure":
            self.figures += 1
            self.figure_visual.append(False)
            self.figure_caption.append(False)
            self.in_figure = True
        elif tag == "figcaption" and self.in_figure: self.in_caption = True
        elif tag == "img":
            src = values.get("src", "")
            if src: self.images.append(src)
            if self.in_figure: self.figure_visual[-1] = True
        elif tag == "svg" and self.in_figure: self.figure_visual[-1] = True
        elif tag == "button": self.buttons += 1
        elif tag == "a":
            href = values.get("href", "")
            if href.startswith("#"): self.anchors.append(href[1:])
        elif tag in ("script", "link"):
            key = "src" if tag == "script" else "href"
            value = values.get(key, "")
            if value and not value.startswith(("http://", "https://", "data:", "#")):
                self.local_assets.append(value)

    def handle_endtag(self, tag):
        if tag == "figure": self.in_figure = False
        elif tag == "figcaption":
            if self.in_figure: self.figure_caption[-1] = bool(self.caption.strip())
            self.caption = ""
            self.in_caption = False

    def handle_data(self, data):
        if self.in_caption: self.caption += data


def validate(path: Path) -> dict:
    parser = ArticleParser()
    source = path.read_text(encoding="utf-8")
    parser.feed(source)
    failures: list[str] = []
    if parser.h1 != 1: failures.append(f"Expected one H1, found {parser.h1}")
    if parser.h2 < 3: failures.append("Expected at least three explanatory sections")
    if not parser.main or not parser.nav: failures.append("Missing semantic main or navigable TOC")
    for key in ("date", "title", "summary", "category"):
        if not parser.metadata.get(key): failures.append(f"Missing journal:{key} metadata")
    if not parser.figures: failures.append("No semantic figures")
    if any(not item for item in parser.figure_visual): failures.append("A figure has no image or SVG")
    if any(not item for item in parser.figure_caption): failures.append("A figure has no explanatory figcaption")
    if parser.buttons < 2: failures.append("Expected at least two interactive controls")
    for anchor in parser.anchors:
        if anchor and anchor not in parser.ids: failures.append(f"Broken local anchor #{anchor}")
    for asset in parser.local_assets + parser.images:
        if not (path.parent / asset.split("#", 1)[0]).resolve().exists():
            failures.append(f"Missing local asset: {asset}")
    if re.search(r"https?://(?:fonts\\.googleapis|fonts\\.gstatic|cdn\\.)", source, re.I):
        failures.append("Remote font/CDN dependency is not allowed")

    svg_results = []
    for svg_path in sorted(path.parent.glob("assets/*.svg")):
        try:
            root = ET.parse(svg_path).getroot()
            names = {node.tag.split("}")[-1] for node in root.iter()}
            if not root.attrib.get("viewBox"): failures.append(f"{svg_path}: missing viewBox")
            if "title" not in names or "desc" not in names: failures.append(f"{svg_path}: missing title/desc")
            svg_results.append(svg_path.name)
        except ET.ParseError as exc:
            failures.append(f"{svg_path}: invalid XML: {exc}")

    return {
        "path": str(path),
        "pass": not failures,
        "counts": {"h2": parser.h2, "figures": parser.figures, "buttons": parser.buttons, "svg_assets": len(svg_results)},
        "svg_assets": svg_results,
        "failures": failures,
    }


def main() -> int:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("html", type=Path)
    argp.add_argument("--report", type=Path)
    args = argp.parse_args()
    result = validate(args.html.resolve())
    import json
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
