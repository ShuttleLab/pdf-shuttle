import type { Metadata, Viewport } from 'next';
import { NextIntlClientProvider } from 'next-intl';
import { getMessages, setRequestLocale, getTranslations } from 'next-intl/server';
import { notFound } from 'next/navigation';
import { localeConfig, type Locale, locales } from '@/lib/i18n/config';
import { generateHomeMetadata } from '@/lib/seo';
import { fontVariables } from '@/lib/fonts';
import { SkipLink } from '@/components/common/SkipLink';
import { ServiceWorkerRegister } from '@/components/sw-register';
import { Toaster } from 'sonner';
import { siteConfig } from '@/config/site';
import '@/app/globals.css';

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

/**
 * Viewport configuration for performance
 * Requirements: 8.1 - Lighthouse performance score 90+
 */
export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  // maximumScale: 5 is WCAG-compliant, but omitting it lets users zoom
  // freely (best a11y). iOS input zoom is handled via font-size >= 16px.
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#0f172a' },
  ],
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  // Validate locale
  const validLocale = locales.includes(locale as Locale) ? (locale as Locale) : 'en';

  // Get localized SEO translations
  const t = await getTranslations({ locale: validLocale, namespace: 'metadata' });

  // Generate metadata using the SEO module with translations
  return generateHomeMetadata(validLocale, {
    title: t('home.title'),
    description: t('home.description'),
  });
}

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  // Validate locale
  if (!locales.includes(locale as Locale)) {
    notFound();
  }

  // Enable static rendering
  setRequestLocale(locale);

  // Get messages for the locale
  const messages = await getMessages();

  // Get direction for the locale
  const direction = localeConfig[locale as Locale]?.direction || 'ltr';

  // SoftwareApplication JSON-LD schema
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "PDF Shuttle",
    applicationCategory: "DeveloperApplication",
    operatingSystem: "Web",
    description: "Free online PDF tools for merging, splitting, compressing, and converting PDF files. All processing happens in your browser for maximum privacy.",
    url: siteConfig.url,
    offers: [
      { "@type": "Offer", name: "Free", price: "0", priceCurrency: "USD" },
    ],
  };

  return (
    <NextIntlClientProvider messages={messages}>
      <div lang={locale} dir={direction} className={`${fontVariables} min-h-screen bg-background text-foreground antialiased font-sans`}>
        <head>
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
          />
        </head>
        <SkipLink targetId="main-content">Skip to main content</SkipLink>
        <ServiceWorkerRegister />
        {children}
        <Toaster position="top-center" richColors closeButton duration={3000} />
      </div>
    </NextIntlClientProvider>
  );
}
