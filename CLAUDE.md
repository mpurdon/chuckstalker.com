# chuckstalker.com

Placeholder-tier gaming-persona landing page for Chuck Stalker. Astro 6 static
site, near-zero JS (two small inline scripts), no Tailwind — custom-property
design tokens + self-hosted fonts. Mirrors the matthewpurdon.me stack.

## Stack facts

- Astro 6, static output to `dist/`, `inlineStylesheets: 'always'` (CSS ships in `<head>`).
- Styles: `src/styles/tokens.css` (two-layer tokens: raw palette → semantic aliases; build UI against semantic only), `base.css` (reset + components), `fonts.css`.
- Fonts: self-hosted latin-subset woff2 in `public/fonts/` — Big Shoulders 800 (display), Allerta Stencil 400 (stencil labels), Barlow 400/500 (body). No CDNs.
- JS budget: the pre-paint random backdrop picker (head) and the hamburger backdrop menu handler (end of body), both inline in `Layout.astro`. Nothing else.

## Background variants

`data-bg` on `<html>`: `black` (default, matches no-JS), `olive`, `rust`,
`gunmetal`. Chosen at random per page load by the head script; `?bg=<name>`
overrides for testing; the masthead hamburger menu lets visitors switch.
Each variant block in `tokens.css` swaps `--bg-base`, `--bg-deep`, and
`--bg-image`. Texture images live in `public/images/bg/bg-<name>.webp`.

Current textures are bootstrapped (patch-quilted in Python from crops of the
logo-preview art — sources and scripts context in `assets-src/`). To upgrade:
generate ~2048×1536+ evenly-lit steel textures with no focal objects,
mid-dark exposure, one per variant, and overwrite the files in
`assets-src/bg/`, then re-export to `public/images/bg/` as webp q72.

## Asset drop-in contract

`assets-src/` holds originals (git-tracked, NOT shipped); `public/images/`
holds optimized exports. When better logo art arrives:

| Path (assets-src) | What | Exported to |
|---|---|---|
| `logo-full-original.png` | Full lockup, transparent, 1254² | `public/images/logo-full.webp` + 800px `.png` fallback |
| `wordmark-banner-keyed-cropped.png` | Nameplate banner, checkerboard keyed out | `public/images/wordmark-banner.webp` (1200w) |
| `logo-mark-circle.png` | Circular mark, transparent | `public/images/logo-mark.webp` (256), `favicon.png`, `apple-touch-icon.png` |
| `greeble-leaf.png` / `greeble-skull.png` | Stamped hull markings (luminance→alpha extractions) | `public/images/greeble-*.webp` |

Gallery: replace the "Awaiting footage" slots in `src/pages/index.astro` with
`<img src="/images/gallery/<name>.webp" alt="..." loading="lazy">`.

Comms: profile URLs + handles are `href="#"` / "Callsign pending" TODOs in
`index.astro` (Steam, PlayStation, Discord).

## Deploy

Push to `main` → GitHub Actions → Cloudflare Pages (project
`chuckstalker-com`). Manual fallback: `npm run deploy`. Verify locally with
`npm run build` before pushing. Repo secrets: `CLOUDFLARE_API_TOKEN`,
`CLOUDFLARE_ACCOUNT_ID`.

## Mockup convention

Design changes get a disposable self-contained HTML mockup in `mockups/`
(screenshots or live preview) approved by the user before production code
changes. `mockups/landing.html` is the approved original.
