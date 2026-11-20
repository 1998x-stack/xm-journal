# xm-journal architecture

## Product boundary

xm-journal is a voice-first personal reflection publishing system. Its only content input is the user's daily spoken reflection or supplied transcript. It does not collect external GitHub activity.

## Sources of truth

- journal/daily/YYYY/MM/YYYY-MM-DD.md: normalized daily text source, preserving the user's meaning.
- posts/YYYY/MM/YYYY-MM-DD/index.html: the Olah-style visual article for that day.
- posts/YYYY/MM/YYYY-MM-DD/assets/: original, article-specific visual assets.
- posts/YYYY/MM/YYYY-MM-DD/evidence.json: provenance for user statements and editorial synthesis.
- skills/olah-style-journal/: the canonical content-production skill.

The Markdown entry is the editorial source. The HTML page is the reader-facing visual artifact. The homepage is generated from article metadata.

## Build flow

~~~text
spoken input
  → interpret and preserve meaning
  → daily Markdown source
  → article narrative + SVG storyboard
  → standalone HTML + interactions + provenance
  → discover article metadata
  → build homepage and copy local assets
  → static validation + Chromium QA
  → GitHub Pages
~~~

## Static publishing

The site is static and offline-first. The build script reads only local posts/**/index.html metadata and copies local files. It does not call GitHub APIs, access sibling repositories, or require secrets.

GitHub Actions runs on pushes, pull requests, or manual dispatch. The workflow performs tests, build, validation, and browser QA. Only the main branch deploys Pages.

## Explicit non-goals

- Cross-repository commit, diff, PR, CI, release, or deployment collection.
- Repository registry, project activity snapshots, or engineering productivity metrics.
- Automatic weekly/monthly rollups and project dashboards.
- Audio recording or speech-to-text infrastructure; speech input is supplied through ChatGPT voice or a transcript.

## Reproducibility

A page can be rebuilt from its committed HTML, assets, and metadata. The homepage index is derived from the article set and is never maintained by hand.
