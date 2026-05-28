import type { NextConfig } from "next";
import { initOpenNextCloudflareForDev } from "@opennextjs/cloudflare";
import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin('./src/i18n/request.ts');

const nextConfig: NextConfig = {
  images: { unoptimized: true },

  // Lint is run separately via `npm run lint` (ESLint flat config).
  // The build's job is compile + type-check; don't fail it on the
  // inherited PDFCraft lint debt (mostly no-explicit-any in WASM/PDF glue).
  eslint: { ignoreDuringBuilds: true },

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

initOpenNextCloudflareForDev();
export default withNextIntl(nextConfig);
