# InstantX Website

Source for the InstantX landing page, published at <https://lf-edge.github.io/instantx/>.

Built with React 19 + Vite + TypeScript. The visual design originates from the
project's design export; the global stylesheet ([src/styles/](src/styles/)) is kept
verbatim from that source — components reference the original class names.

## Develop

```bash
npm ci
npm run dev        # http://localhost:5173/instantx/  (note the /instantx/ base)
```

## Build & preview

```bash
npm run lint
npm run build      # type-checks, then bundles to dist/
npm run preview    # http://localhost:4173/instantx/  (production bundle)
```

The Vite `base` is hardcoded to `/instantx/` because the site is served as a
GitHub Pages project site — keep it in sync if the repository is ever renamed.

## Deploy

`.github/workflows/website.yml` builds on every PR touching `website/**` and
deploys to GitHub Pages on push to `main` (plus manual `workflow_dispatch`).
