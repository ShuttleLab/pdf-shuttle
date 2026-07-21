'use client';

import React from 'react';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { Lock, Shield } from 'lucide-react';
import { type Locale } from '@/lib/i18n/config';

export interface FooterProps {
  locale: Locale;
}

// Sibling ShuttleLab products for cross-promotion (handbook §13 convention).
// English-only labels — these are brand names + universally short descriptions
// that work across all 14 supported locales without translation overhead.
const SHUTTLELAB_PRODUCTS: Array<{ href: string; emoji: string; name: string }> = [
  { href: 'https://ppt.shuttlelab.org', emoji: '📽️', name: 'PPT' },
  { href: 'https://note.shuttlelab.org', emoji: '📝', name: 'Note' },
  { href: 'https://status.shuttlelab.org', emoji: '📊', name: 'Status' },
  { href: 'https://pdf2docx.shuttlelab.org', emoji: '📘', name: 'PDF2Word' },
  { href: 'https://clipboard.shuttlelab.org', emoji: '📋', name: 'Clipboard' },
  { href: 'https://file.shuttlelab.org', emoji: '📁', name: 'File' },
  { href: 'https://json.shuttlelab.org', emoji: '✓', name: 'JSON' },
  { href: 'https://yaml.shuttlelab.org', emoji: '⚙️', name: 'YAML' },
  { href: 'https://msg.shuttlelab.org', emoji: '💬', name: 'Message' },
  { href: 'https://docx.shuttlelab.org', emoji: '📑', name: 'Docx' },
  { href: 'https://image.shuttlelab.org', emoji: '🖼️', name: 'Image' },
  { href: 'https://diff.shuttlelab.org', emoji: '🔀', name: 'Diff' },
  { href: 'https://qr.shuttlelab.org', emoji: '📱', name: 'QR' },
  { href: 'https://base64.shuttlelab.org', emoji: '🔤', name: 'Base64' },
  { href: 'https://url.shuttlelab.org', emoji: '🔗', name: 'URL' },
  { href: 'https://regex.shuttlelab.org', emoji: '🔣', name: 'Regex' },
  { href: 'https://time.shuttlelab.org', emoji: '⏱️', name: 'Time' },
];

export const Footer: React.FC<FooterProps> = ({ locale }) => {
  const t = useTranslations('common');
  const currentYear = new Date().getFullYear();

  const navLinks = [
    { href: `/${locale}/about`, label: t('navigation.about') },
    { href: `/${locale}/faq`, label: t('navigation.faq') },
    { href: `/${locale}/privacy`, label: t('navigation.privacy') },
    { href: `/${locale}/terms`, label: t('navigation.terms') || 'Terms' },
    { href: `/${locale}/contact`, label: t('navigation.contact') },
  ];

  return (
    <footer
      className="w-full bg-[hsl(var(--color-muted)/0.4)] border-t border-[hsl(var(--color-border))]"
      role="contentinfo"
    >
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center gap-3 text-sm text-[hsl(var(--color-muted-foreground))]">
          {/* Row 1: Trust line (privacy positioning, compact) */}
          <p className="flex items-center gap-2 text-xs flex-wrap justify-center">
            <Lock className="h-3 w-3 text-[hsl(var(--color-success))] flex-shrink-0" aria-hidden="true" />
            <span>{t('footer.trustFiles') || 'Files never leave your device'}</span>
            <span className="text-[hsl(var(--color-muted-foreground))/0.4]">·</span>
            <Shield className="h-3 w-3 text-[hsl(var(--color-success))] flex-shrink-0" aria-hidden="true" />
            <span>{t('footer.trustPrivacy') || 'GDPR compliant · 100% private'}</span>
          </p>

          {/* Row 2: Pipe-separated nav links — matches note-shuttle convention */}
          <div className="flex items-center gap-3 flex-wrap justify-center">
            {navLinks.map((link, idx) => (
              <React.Fragment key={link.href}>
                {idx > 0 && (
                  <span className="text-[hsl(var(--color-muted-foreground))/0.3]" aria-hidden="true">
                    |
                  </span>
                )}
                <Link
                  href={link.href}
                  className="hover:text-[hsl(var(--color-foreground))] transition-colors"
                >
                  {link.label}
                </Link>
              </React.Fragment>
            ))}
          </div>

          {/* Row 3: Cross-promotion — "Also from ShuttleLab: X · Y · Z" (note's pattern) */}
          <p className="flex items-center gap-2 flex-wrap justify-center text-xs">
            <span className="text-[hsl(var(--color-muted-foreground))/0.8]">
              {t('footer.alsoFrom') || 'Also from ShuttleLab:'}
            </span>
            {SHUTTLELAB_PRODUCTS.map((product, idx) => (
              <React.Fragment key={product.href}>
                {idx > 0 && (
                  <span className="text-[hsl(var(--color-muted-foreground))/0.3]" aria-hidden="true">
                    ·
                  </span>
                )}
                <a
                  href={product.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-medium text-[hsl(var(--color-foreground))] hover:text-[hsl(var(--color-primary))] transition-colors"
                >
                  <span aria-hidden="true">{product.emoji}</span> {product.name}
                </a>
              </React.Fragment>
            ))}
          </p>

          {/* Row 4: Copyright + personality signature + AGPL §13 source link */}
          <div className="pt-3 mt-1 border-t border-[hsl(var(--color-border))/0.5] w-full max-w-2xl text-center text-xs space-y-1">
            <p>
              &copy; {currentYear}{' '}
              <span data-testid="footer-brand-name" className="font-medium text-[hsl(var(--color-foreground))]">
                {t('brand')}
              </span>{' '}
              ·{' '}
              <span className="text-[hsl(var(--color-muted-foreground))/0.8]">
                {t('footer.signature') || 'Made with care · No ads, no tracking, no nonsense.'}
              </span>
            </p>
            <p className="text-[hsl(var(--color-muted-foreground))/0.7]">
              <a
                href="https://github.com/ShuttleLab/pdf-shuttle"
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:text-[hsl(var(--color-foreground))]"
              >
                {t('footer.sourceCode') || 'Source code'}
              </a>{' '}
              (AGPL-3.0) ·{' '}
              <a
                href="mailto:support@shuttlelab.org"
                className="hover:text-[hsl(var(--color-foreground))] transition-colors"
              >
                support@shuttlelab.org
              </a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
