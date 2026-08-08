# AGENTS.md

PDF Shuttle: fully client-side PDF toolkit (90+ tools) — Next.js 15 (App Router) + React 19 + TS + Tailwind 4. **All PDF processing runs in the browser**; files never leave the device. Fork of PDFCraft (AGPL-3.0), see `NOTICE.md`. Deployed as static export on Cloudflare Workers via Wrangler. (Detailed architecture notes also live in `CLAUDE.md`; `AGENTS.md` is the compact version.)

## Commands

```bash
npm run dev            # dev server (Turbopack) on :3000
npm run build          # static export to ./out (output: "export")
npm run lint           # ESLint flat config
npm test               # vitest run (all)
npx vitest run src/__tests__/lib/foo.test.ts   # single file
npx vitest run -t "name substring"             # single test
npm run deploy         # build + wrangler deploy
npm run preview        # build + wrangler dev
```

- **Lint is decoupled from the build**: `next.config.ts` sets `eslint.ignoreDuringBuilds: true`. The build only compiles + type-checks. Most lint rules are `warn` (inherited PDFCraft `no-explicit-any` debt in WASM/PDF glue); treat **type errors as the real gate**.
- **No server runtime** (`output: "export"`): no API routes, no server actions, no `next start` in prod. Everything must be static HTML + client JS.
- `wrangler.toml` serves `./out` as static assets (`not_found_handling = "404-page"`).

## Architecture: three layers per tool

Every tool is keyed by a stable `id` and exists in three parallel places — **all must be updated when adding a tool**:

1. `src/config/tools.ts` — registry (`id`, `slug`, `icon`, `category`, formats, features, related).
2. `src/lib/pdf/processors/*.ts` — pure logic extending `BasePDFProcessor` (`src/lib/pdf/processor.ts`); exported from `processors/index.ts`.
3. `src/components/tools/<tool>/` — React UI (93 dirs).

Routing: `src/app/[locale]/tools/[tool]/page.tsx` imports every component and maps `tool.id` via a big `switch` in `renderToolInterface()` — wire new tool ids in there too. `generateStaticParams()` pre-renders all tools × locales.

## PDF libraries: lazy, often in workers

- Loaders in `src/lib/pdf/`: `loader.ts` (pdf-lib + pdf.js, worker `/workers/pdf.worker.min.mjs`), `loader-legacy.ts` (pdfjs-dist v2 aliased `pdfjs-dist-legacy`), `pymupdf-loader.ts` (PyMuPDF via Pyodide from `public/pymupdf-wasm/`), `qpdf-loader.ts` (`public/qpdf.wasm`).
- Heavy tools ship **prebuilt** web workers in `public/workers/*.worker.js` (compress, ocr, epub-to-pdf, pdf-to-docx, …). WASM/worker assets are static files, **not bundled**; `next.config.ts` stubs Node built-ins for the browser (`fs`, `path`, `crypto`, `canvas`…) and enables `asyncWebAssembly`.
- Dev quirk: Turbopack ignores the `webpack()` config, so the `require("canvas")` in `pdfjs-dist-legacy` would 500 tool routes in dev — `next.config.ts` aliases `canvas` to `src/lib/stubs/empty.ts` under `turbopack.resolveAlias`. Keep that stub working.

## i18n (next-intl) — 12 locales, two content systems

Locales (from `src/lib/i18n/config.ts`, not the stale "14" in README): `en, ja, ko, es, fr, de, zh, zh-TW, pt, ar, it, id`. `localePrefix: 'as-needed'` — English at `/`, others at `/zh/` etc.

A new user-facing string must go in **both**:
- **UI strings**: `messages/<locale>.json` (merged w/ English fallback via `src/lib/i18n/fallback.ts`).
- **Tool page SEO content** (titles, descriptions, FAQ, how-to): `src/config/tool-content/<locale>.ts`; `zh-TW` falls back to `zh`.

## Conventions & gotchas

- Path aliases: `@/*` → `src/*` (`@/components`, `@/lib`, `@/types`, `@/config`, `@/messages`); mirrored in `tsconfig.json` + `vitest.config.ts`.
- For subpath deployments set `NEXT_PUBLIC_BASE_PATH`. Manual `fetch` of public assets (workers, WASM) must go through `withBasePath()` from `src/lib/utils/path.ts` — Next only auto-handles `Link`/`Image`.
- State: Zustand; IndexedDB persistence (`src/lib/storage/`).
- SEO: per-tool JSON-LD in `src/lib/seo/`, injected by `src/components/seo/JsonLd.tsx`.
- Workflow engine: `src/lib/workflow/` (DAG in `engine.ts`, runner in `executor.ts`), ReactFlow canvas at `src/app/[locale]/workflow/`, templates in `src/config/workflow-templates.ts`.

## Testing

vitest + jsdom + Testing Library in `src/__tests__/` (`components/`, `lib/`, `workflow/`, `accessibility/`; **property tests with fast-check live in `src/__tests__/properties/`**). `fake-indexeddb` backs storage tests. Setup in `src/__tests__/setup.ts`.

## Legal

AGPL-3.0 fork with attribution obligations — keep modifications documented in `NOTICE.md`.