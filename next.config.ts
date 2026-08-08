import type { NextConfig } from "next";
import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin('./src/i18n/request.ts');

const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  // Canonical URLs carry a trailing slash (e.g. /en/, /en/tools/merge-pdf/).
  // The static export then emits `<route>/index.html` so hosters serve the
  // slash version directly (200) instead of 307-redirecting to the
  // no-slash variant, which Google refuses to index / pass equity to.
  trailingSlash: true,

  // Lint is run separately via `npm run lint` (ESLint flat config).
  // The build's job is compile + type-check; don't fail it on the
  // inherited PDFCraft lint debt (mostly no-explicit-any in WASM/PDF glue).
  eslint: { ignoreDuringBuilds: true },

  // Turbopack (dev) does NOT use the webpack() config below, so the Node-only
  // `require("canvas")` in pdfjs-dist-legacy 500s every tool route in
  // `next dev --turbopack`. Alias it to an empty stub — it's never called in
  // the browser. Production (webpack, below) already stubs it via IgnorePlugin.
  turbopack: {
    resolveAlias: {
      canvas: './src/lib/stubs/empty.ts',
    },
  },

  // Webpack configuration for WASM modules
  webpack: (config, { isServer, webpack }) => {
    // Handle modules that use Node.js built-ins
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
        crypto: false,
        module: false,
        url: false,
        worker_threads: false,
        canvas: false,
      };
    } else {
      config.externals = config.externals || [];
      config.externals.push({
        canvas: 'commonjs canvas',
      });
    }

    config.resolve.alias = {
      ...config.resolve.alias,
      'module': false,
    };

    config.plugins.push(
      new webpack.IgnorePlugin({
        resourceRegExp: /^module$/
      }),
      new webpack.IgnorePlugin({
        resourceRegExp: /^canvas$/,
        contextRegExp: /pdfjs-dist-legacy/
      })
    );

    // Enable WebAssembly
    config.experiments = {
      ...config.experiments,
      asyncWebAssembly: true,
    };

    return config;
  },
};

export default withNextIntl(nextConfig);
