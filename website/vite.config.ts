import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Deployed at https://lf-edge.github.io/instantx/ — the base path is mandatory
// for assets to resolve on a GitHub Pages project site. Hardcoded (not
// env-driven) so `npm run dev` and `npm run preview` exercise the real base
// path locally and surface 404s before CI.
export default defineConfig({
  plugins: [react()],
  base: '/instantx/',
})
