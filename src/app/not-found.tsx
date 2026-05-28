import Link from 'next/link';
import { getTranslations } from 'next-intl/server';
import { routing } from '@/i18n/routing';

// Root-level 404 — Next.js static export uses THIS for the catch-all
// out/404.html that Cloudflare Workers serves on any unmatched URL.
// We hardcode English (defaultLocale) because there's no locale context
// at the root level; localized 404s for in-app navigation are handled by
// src/app/[locale]/not-found.tsx.
export default async function RootNotFound() {
  const defaultLocale = routing.defaultLocale;
  const t = await getTranslations({ locale: defaultLocale, namespace: 'notFound' });

  const popularTools: Array<{
    slug: string;
    key: 'mergePdf' | 'splitPdf' | 'compressPdf' | 'pdfToJpg' | 'jpgToPdf';
  }> = [
    { slug: 'merge-pdf', key: 'mergePdf' },
    { slug: 'split-pdf', key: 'splitPdf' },
    { slug: 'compress-pdf', key: 'compressPdf' },
    { slug: 'pdf-to-jpg', key: 'pdfToJpg' },
    { slug: 'jpg-to-pdf', key: 'jpgToPdf' },
  ];

  return (
    <html lang={defaultLocale}>
      <body>
        <div className="min-h-screen flex items-center justify-center px-4 py-16 bg-[hsl(var(--color-background))]">
          <div className="text-center max-w-lg">
            <div className="text-7xl mb-4" aria-hidden="true">
              {t('emoji')}
            </div>
            <h1 className="text-5xl font-bold mb-3 text-[hsl(var(--color-foreground))]">
              {t('code')}
            </h1>
            <p className="text-lg text-[hsl(var(--color-foreground))] mb-2">{t('title')}</p>
            <p className="text-sm text-[hsl(var(--color-muted-foreground))] mb-8 leading-relaxed">
              {t('description')}
            </p>

            <Link
              href={`/${defaultLocale}`}
              className="inline-block px-6 py-2.5 bg-[hsl(var(--color-foreground))] text-[hsl(var(--color-background))] rounded-md hover:opacity-90 transition-opacity"
            >
              {t('cta')}
            </Link>

            <div className="mt-12 pt-8 border-t border-[hsl(var(--color-border))]">
              <p className="text-xs uppercase tracking-wider text-[hsl(var(--color-muted-foreground))/0.7] mb-3">
                {t('popularToolsHeading')}
              </p>
              <div className="flex flex-wrap gap-x-3 gap-y-2 justify-center text-sm">
                {popularTools.map((tool, idx) => (
                  <span key={tool.slug} className="flex items-center gap-3">
                    {idx > 0 && (
                      <span className="text-[hsl(var(--color-muted-foreground))/0.3]" aria-hidden="true">
                        ·
                      </span>
                    )}
                    <Link
                      href={`/${defaultLocale}/tools/${tool.slug}`}
                      className="text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-primary))] transition-colors"
                    >
                      {t(`tools.${tool.key}`)}
                    </Link>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}
