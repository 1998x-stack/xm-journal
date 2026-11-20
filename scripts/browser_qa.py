"""Run the Olah-style Chromium QA protocol for every daily visual article."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"
CHECKER_PATH = ROOT / "skills" / "olah-style-journal" / "scripts" / "browser_check.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("olah_journal_browser_check", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load browser checker: {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    articles = sorted(POSTS.glob("**/index.html"))
    if not articles:
        print("No visual articles found; browser QA skipped.")
        return 0

    checker = load_checker()
    results = []
    with sync_playwright() as playwright:
        browser = checker.launch_browser(playwright)
        try:
            for article in articles:
                relative = article.parent.relative_to(POSTS).as_posix().replace("/", "-")
                output = ROOT / "_qa" / relative
                result = checker.check_article(article, output, browser)
                results.append(result)
        finally:
            browser.close()

    failed = [item for item in results if not item.get("pass")]
    for item in results:
        print(f"{'PASS' if item.get('pass') else 'FAIL'} {item['file']}")
    print(f"Browser QA: {len(results) - len(failed)}/{len(results)} article(s) passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
