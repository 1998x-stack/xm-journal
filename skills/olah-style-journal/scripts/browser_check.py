#!/usr/bin/env python3
"""Real Chromium viewport, interaction and print checks for one local journal article."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

SIZES = [("desktop", 1440, 900), ("tablet", 768, 1024), ("mobile", 390, 844), ("narrow-mobile", 360, 800)]


def launch_browser(playwright):
    configured = Path(os.getenv("CHROMIUM_PATH", "/usr/bin/chromium"))
    options = {"executable_path": str(configured)} if configured.exists() else {}
    return playwright.chromium.launch(headless=True, args=["--no-sandbox"], **options)


def check_article(page_file: Path, output: Path, browser, click: str = "button") -> dict:
    page_file = Path(page_file).resolve()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    report = {"file": str(page_file), "pass": True, "viewports": {}, "errors": [], "interaction": {}}

    for label, width, height in SIZES:
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda error, log=errors: log.append(str(error)))
        page.on("console", lambda message, log=errors: log.append("console: " + message.text) if message.type == "error" else None)
        page.route("https?://**", lambda route: route.abort())
        page.goto(page_file.as_uri(), wait_until="load")
        page.screenshot(path=str(output / f"{label}.png"), full_page=False)
        measure = page.evaluate("""() => ({
          scrollWidth: document.documentElement.scrollWidth,
          viewport: innerWidth,
          heading: document.querySelectorAll('h1').length,
          blankSVG: [...document.querySelectorAll('svg')].filter(s => {
            const r = s.getBoundingClientRect(); return r.width < 1 || r.height < 1;
          }).length,
          brokenImages: [...document.images].filter(i => !i.complete || i.naturalWidth < 1).length,
          controls: [...document.querySelectorAll('button')].filter(b => !b.getAttribute('aria-label') && !b.textContent.trim()).length
        })""")
        okay = (
            measure["scrollWidth"] <= measure["viewport"] + 1
            and measure["heading"] == 1
            and measure["blankSVG"] == 0
            and measure["brokenImages"] == 0
            and measure["controls"] == 0
            and not errors
        )
        report["viewports"][label] = {**measure, "pass": okay, "errors": errors}
        if not okay:
            report["pass"] = False

        if label == "desktop":
            buttons = page.locator(click)
            if buttons.count() >= 2:
                before = page.content()
                changed = False
                for index in range(min(6, buttons.count())):
                    try:
                        buttons.nth(index).click(timeout=1500)
                        if page.content() != before:
                            changed = True
                            break
                    except Exception as exc:
                        errors.append("interaction: " + str(exc)[:160])
                report["interaction"] = {"status": "verified" if changed else "failed", "buttons": buttons.count()}
                if not changed:
                    report["pass"] = False
            else:
                report["interaction"] = {"status": "missing", "buttons": buttons.count()}
                report["pass"] = False
            page.emulate_media(media="print")
            page.screenshot(path=str(output / "print.png"), full_page=False)
        page.close()

    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--click", default="button")
    args = parser.parse_args()
    with sync_playwright() as playwright:
        browser = launch_browser(playwright)
        try:
            report = check_article(args.html, args.output, browser, args.click)
        finally:
            browser.close()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
