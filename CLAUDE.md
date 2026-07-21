# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

PDF Shuttle is a fully client-side PDF toolkit (90+ tools) built on Next.js 15 (App Router) + React 19 + TypeScript + Tailwind 4. **All PDF processing runs in the browser** — files never leave the device. It is a fork of PDFCraft (AGPL-3.0); see `NOTICE.md`. Deployed as a static export to Cloudflare Workers via Wrangler.

## Commands

```bash
npm run dev            # dev server (Turbopack) on :3000
npm run build          # next build → static export to ./out (output: "export")
npm run lint           # ESLint flat config (NOT run during build — see below)
npm test               # vitest run (all tests)
npm run test:watch     # vitest watch mode
npm run test:coverage  # v8 coverage
npm run deploy         # build + wrangler deploy to Cloudflare
npm run preview        # build + wrangler dev (local Workers preview)
```

Run a single test file or test:
```bash
npx vitest run src/__tests__/lib/foo.test.ts
npx vitest run -t "test name substring"
```

Notes:
- **Lint is decoupled from build.** `next.config.ts` sets `eslint.ignoreDuringBuilds: true` — the build only compiles + type-checks. Run `npm run lint` separately. Most lint rules are `warn` (inherited PDFCraft debt, mostly `no-explicit-any` in WASM/PDF glue), so lint rarely fails CI; prefer type errors as the real gate.
- `output: "export"` means **no server runtime** — no API routes, no server actions, no `next start` in production. Everything must work as static HTML + client JS.

## Architecture

### Three layers: config → processor → component

Each tool is defined in three parallel places, keyed by a stable tool `id`:

1. **`src/config/tools.ts`** — the tool registry. Every tool is a `Tool` object with `id`, `slug`, `icon`, `category` (one of 6), `acceptedFormats`, `outputFormat`, `maxFiles`, `features`, `relatedTools`. This is the source of truth for what tools exist.
2. **`src/lib/pdf/processors/*.ts`** — the pure processing logic. Processors extend `BasePDFProcessor` (`src/lib/pdf/processor.ts`), which provides validation, progress, and cancellation. All exported from `src/lib/pdf/processors/index.ts`.
3. **`src/components/tools/<tool>/`** — the React UI for each tool (93 component dirs).

Routing ties them together in **`src/app/[locale]/tools/[tool]/page.tsx`**: it imports every tool component, then a big `switch (tool.id)` in `renderToolInterface()` maps id → component. `generateStaticParams()` pre-renders every tool × every locale at build time.

**To add a tool** you touch all three layers: register in `tools.ts`, add a processor + export it from `processors/index.ts`, add a component dir, wire the id into the `switch` in `[tool]/page.tsx`, and add localized content (below).

### PDF processing libraries (lazy-loaded)

No PDF library is loaded until a tool needs it. Loaders live in `src/lib/pdf/`:
- `loader.ts` — pdf-lib (create/modify) and pdf.js (render). Also configures the pdf.js worker (`/workers/pdf.worker.min.mjs`).
- `loader-legacy.ts` — pdfjs-dist v2 legacy build (aliased as `pdfjs-dist-legacy` in package.json) for cases the v4 build can't handle.
- `pymupdf-loader.ts` — PyMuPDF via Pyodide (WASM) from `public/pymupdf-wasm/`.
- `qpdf-loader.ts` — qpdf WASM (`public/qpdf.wasm`) for encrypt/decrypt/linearize.

Heavy tools also run in dedicated **web workers** shipped as prebuilt files in `public/workers/*.worker.js` (compress, ocr, epub-to-pdf, etc.). WASM/worker assets are static files under `public/`, not bundled — `next.config.ts` stubs Node built-ins (`fs`, `path`, `crypto`, `canvas`…) for the browser and enables `asyncWebAssembly`.

### i18n (next-intl)

14 locales. `localePrefix: 'as-needed'` — English is at `/`, others at `/zh/`, `/ja/`, etc. Routing config in `src/i18n/routing.ts`; locale list in `src/lib/i18n/config.ts`.

Two separate content systems, **both must be updated** for a new user-facing string:
- **UI strings**: `messages/<locale>.json` (loaded via `src/i18n/request.ts`). Missing keys fall back to English via `mergeWithFallback` (`src/lib/i18n/fallback.ts`).
- **Tool page content** (titles, descriptions, FAQ, how-to for SEO): `src/config/tool-content/<locale>.ts`, aggregated in `tool-content/index.ts`. `getToolContent(locale, id)` falls back to English; `zh-TW` falls back to `zh`.

### Workflow engine

`src/lib/workflow/` implements a node-graph pipeline (chain multiple tools). `engine.ts` builds a DAG and does topological sort (cycle detection → null); `executor.ts` runs it. UI is a ReactFlow canvas under `src/components/workflow/` and `src/app/[locale]/workflow/`. Templates in `src/config/workflow-templates.ts`.

### Other conventions

- **Path aliases**: `@/*` → `src/*` (plus `@/components`, `@/lib`, `@/types`, `@/config`, `@/messages`). Defined in both `tsconfig.json` and `vitest.config.ts`.
- **basePath**: for subpath deployments set `NEXT_PUBLIC_BASE_PATH`. Manual `fetch` of public assets (workers, WASM) must go through `withBasePath()` in `src/lib/utils/path.ts` — Next only auto-handles `Link`/`Image`.
- **State**: Zustand. Client-side persistence via IndexedDB (`src/lib/storage/project-db.ts`, `recent-files.ts`).
- **SEO**: structured data (JSON-LD) generated per tool in `src/lib/seo/`; injected via `src/components/seo/JsonLd.tsx`.
- **Tests**: vitest + jsdom + Testing Library, in `src/__tests__/` (`components/`, `lib/`, `workflow/`, `accessibility/`, `properties/` — the last uses fast-check property tests). `fake-indexeddb` backs storage tests.
