# Publishing a daily visual journal

1. Confirm the Markdown source and HTML article represent the same spoken input.
2. Check the article metadata, unique visual assets, evidence record and local links.
3. Run python -m pytest -q, python scripts/build_site.py, python scripts/validate_site.py, and python scripts/browser_qa.py.
4. Review the article on desktop and mobile; verify keyboard interaction and print layout.
5. Commit the daily source, article and assets to the repository.
6. GitHub Actions builds and deploys the static site from main.
7. Claim that the article is live only after the Pages deployment job succeeds. A commit or successful build alone is not proof of deployment.

The workflow has no schedule and no GitHub token for reading sibling repositories. It only builds and publishes the journal itself.
