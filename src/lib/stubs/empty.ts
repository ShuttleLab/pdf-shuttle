/**
 * Empty stub module.
 *
 * Turbopack (used by `next dev --turbopack`) does not read the `webpack()`
 * config in next.config.ts, so the Node-only `require("canvas")` inside
 * pdfjs-dist-legacy fails to resolve and 500s every tool route in dev.
 * We alias `canvas` to this stub for Turbopack; it is never called in the
 * browser (it lives in a NodeCanvasFactory code path that only runs in Node).
 */
export default {};
