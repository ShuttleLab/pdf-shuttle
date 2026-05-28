import Link from 'next/link';
import { getTranslations, setRequestLocale } from 'next-intl/server';
import { routing } from '@/i18n/routing';

// Statically generate /[locale]/not-found per locale so each language's 404
// renders with its own translated copy.
export async function generateStaticParams() {
  return routing.locales.map((locale) => ({ locale }));
}

interface NotFoundProps {
  params?: Promise<{ locale: string }>;
}

export default async function NotFound({ params }: NotFoundProps) {
  // For statically rendered not-found, locale comes from params.
  // Fallback to defaultLocale when called outside the [locale] segment.
  const locale = (params ? (await params).locale : routing.defaultLocale) as string;
  setRequestLocale(locale);
  const t = await getTranslations({ locale, namespace: 'notFound' });

  // Top 5 popular tools — high-conversion cross-promotion when users hit 404.
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
    <div className="flex flex-1 items-center justify-center px-4 py-16">
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
          href={`/${locale}`}
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
                  href={`/${locale}/tools/${tool.slug}`}
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
  );
}
