# LeanEdge

Website for **LeanEdge Consulting**: Elias Hanna, operational excellence, Lean Six Sigma, process improvement and reporting automation. Live at <https://leanedge.si>.

It's a plain static site (HTML, CSS and a little JavaScript). There's no framework, no build step and no trackers. GitHub Pages serves the `main` branch as-is.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The whole one-page site: hero, results, services, experience, approach, about, engagements, contact |
| `404.html` | Not-found page (uses root-relative paths because Pages serves it for any missing URL) |
| `assets/css/styles.css` | All styles; colours and spacing are tokens at the top (`--navy` is sampled from the logo) |
| `assets/js/main.js` | Mobile menu, header shadow, reveal-on-scroll, active nav link, footer year |
| `assets/img/` | Logo SVGs (stacked, horizontal, mark; navy and white), favicons, social card, photo placeholder |
| `assets/fonts/` | Inter (400/600/700), self-hosted, SIL Open Font License |
| `assets/docs/LeanEdge_Consulting_Profile.pdf` | Downloadable profile |
| `CNAME` | Custom domain for GitHub Pages (`leanedge.si`) |
| `tools/make_logo.py` | Regenerates the logo SVGs and PNG favicons (`pip install fonttools brotli pillow`) |
| `tools/render_images.ps1` | Re-renders `og-image.png` from `tools/render/og-image.html` with headless Edge |

## Common edits

- **Text:** edit `index.html` directly.
- **Elias's photo:** save it as `assets/img/elias.jpg` (portrait, about 480×560) and change the `src` of the About image in `index.html` from `elias-placeholder.svg` to `elias.jpg`.
- **Profile PDF:** replace `assets/docs/LeanEdge_Consulting_Profile.pdf`, keeping the same name.
- **Preview locally:** run `python -m http.server 8791` in the repo root, then open <http://127.0.0.1:8791>.

## Deploying

Push to `main`. GitHub Pages (Settings → Pages → Deploy from branch `main`, folder `/`) publishes within a minute or two.

DNS for `leanedge.si` is managed in Hostinger hPanel:

- `A @` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- `CNAME www` → `abdojk.github.io`
