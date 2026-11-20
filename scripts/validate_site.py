"""Validate journal data and generated report structure."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def main():
    for rel in ("data/entries.json","data/taxonomy.json","reports/index.json","config/projects.json"):
        json.loads((ROOT/rel).read_text(encoding="utf-8"))
    out=ROOT/"_site/index.html"
    if not out.exists(): raise SystemExit("Run scripts/build_site.py first")
    html=out.read_text(encoding="utf-8")
    if html.count("<h1") != 1: raise SystemExit("Homepage must contain exactly one H1")
    if "assets/app.js" not in html: raise SystemExit("Homepage dashboard loader is missing")
    for report in (ROOT/"_site/reports").glob("**/*.html"):
        text=report.read_text(encoding="utf-8")
        if text.count("<h1") != 1: raise SystemExit(f"Report must contain exactly one H1: {report}")
        if "report.css" not in text: raise SystemExit(f"Report stylesheet missing: {report}")
    print("Validation passed")
if __name__=="__main__": main()
