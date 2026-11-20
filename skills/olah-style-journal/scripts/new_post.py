#!/usr/bin/env python3
"""Create a daily visual journal article scaffold from the Olah-style template."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--dek", default="从今天真实发生的一件事开始，逐步看清它背后的问题与变化。")
    parser.add_argument("--category", default="reflection")
    parser.add_argument("--category-label", default="复盘与思考")
    parser.add_argument("--tags", default="")
    args = parser.parse_args()

    try:
        day = date.fromisoformat(args.date)
    except ValueError:
        parser.error("--date must be YYYY-MM-DD")
    if not args.title.strip() or not args.summary.strip():
        parser.error("--title and --summary cannot be blank")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.category):
        parser.error("--category must be lowercase kebab-case")

    destination = REPO_ROOT / "posts" / f"{day.year:04d}" / f"{day.month:02d}" / day.isoformat()
    destination.mkdir(parents=True, exist_ok=True)
    template = (SKILL_ROOT / "assets" / "templates" / "article.html").read_text(encoding="utf-8")
    values = {
        "{{DATE}}": day.isoformat(),
        "{{TITLE}}": args.title,
        "{{SUMMARY}}": args.summary,
        "{{CATEGORY}}": args.category,
        "{{CATEGORY_LABEL}}": args.category_label,
        "{{TAGS}}": args.tags,
        "{{DEK}}": args.dek,
        "{{CSS_PATH}}": "../../../../skills/olah-style-journal/assets/css/article.css",
        "{{JS_PATH}}": "../../../../skills/olah-style-journal/assets/js/interactions.js",
        "{{TOC}}": '<strong>今日复盘</strong><a href="#opening">今天发生了什么</a><a href="#insight">核心感悟</a><a href="#action">下一步</a>',
    }
    for token, value in values.items():
        template = template.replace(token, value)
    output = destination / "index.html"
    if output.exists():
        parser.error(f"Refusing to overwrite existing article: {output}")
    output.write_text(template, encoding="utf-8")
    (destination / "evidence.json").write_text(
        '{"source":{"id":"voice-' + day.isoformat() + '","type":"user-provided spoken reflection"},'
        '"claims":[]}\\n',
        encoding="utf-8",
    )
    print(f"Created {output.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
