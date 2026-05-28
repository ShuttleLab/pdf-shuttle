'use client';

import React from 'react';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { Shield, Lock, Github, Mail } from 'lucide-react';
import { type Locale } from '@/lib/i18n/config';

export interface FooterProps {
  locale: Locale;
}

// Sibling ShuttleLab products for cross-promotion (P1: handbook §13 convention).
// Descriptions are English-only — they're brand-adjacent content where keeping
// English is internationally acceptable. Can be moved to messages/*.json later
// if per-locale taglines are desired.
const SHUTTLELAB_PRODUCTS: Array<{
  href: string;
  emoji: string;
  name: string;
  desc: string;
}> = [
  { href: 'https://shuttlelab.org', emoji: '🚀', name: 'ShuttleLab Hub', desc: 'All free tools' },
  { href: 'https://note.shuttlelab.org', emoji: '📝', name: 'Note Shuttle', desc: 'Encrypted markdown notes' },
  { href: 'https://status.shuttlelab.org', emoji: '📊', name: 'Status Shuttle', desc: 'Uptime monitoring & alerts' },
  { href: 'https://json.shuttlelab.org', emoji: '✓', name: 'JSON Shuttle', desc: 'JSON validator & formatter' },
  { href: 'https://yaml.shuttlelab.org', emoji: '⚙️', name: 'YAML Shuttle', desc: 'YAML formatter & converter' },
];

export const Footer: React.FC<FooterProps> = ({ locale }) => {
  const t = useTranslations('common');
  const currentYear = new Date().getFullYear();

  const resourceLinks = [
    { href: `/${locale}/about`, label: t('navigation.about') },
    { href: `/${locale}/faq`, label: t('navigation.faq') },
    { href: `/${locale}/privacy`, label: t('navigation.privacy') },
    { href: `/${locale}/terms`, label: t('navigation.terms') || 'Terms' },
    { href: `/${locale}/contact`, label: t('navigation.contact') },
  ];

  return (
    <footer
      className="w-full border-t border-[hsl(var(--color-border))] bg-[hsl(var(--color-background))] pt-12 pb-8"
      role="contentinfo"
    >
      <div className="container mx-auto px-4">
        {/* 3-column grid: Brand+trust | Resources | Other ShuttleLab tools */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 md:gap-12 mb-10">
          {/* Column 1: Brand + tagline + trust + social */}
          <div className="flex flex-col gap-5">
            <Link
              href={`/${locale}`}
              className="group flex items-center gap-2.5 text-xl font-bold text-[hsl(var(--color-foreground))]"
              aria-label={`${t('brand')} - ${t('navigation.home')}`}
            >
              <div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-[hsl(var(--color-primary))] text-white shadow-md transition-transform group-hover:scale-105">
                <svg
                  className="h-5 w-5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                  <polyline points="14 2 14 8 20 8" />
                </svg>
              </div>
              <span data-testid="footer-brand-name">{t('brand')}</span>
            </Link>

            <p className="text-sm text-[hsl(var(--color-muted-foreground))] leading-relaxed max-w-xs">
              {t('tagline') || 'Professional, secure, and free PDF tools for everyone. No installation required.'}
            </p>

            {/* Compact trust badges (inline, no separate columns) */}
            <ul className="flex flex-col gap-2 text-xs text-[hsl(var(--color-muted-foreground))]">
              <li className="flex items-center gap-2">
                <Lock className="h-3.5 w-3.5 text-[hsl(var(--color-success))] flex-shrink-0" aria-hidden="true" />
                <span>Client-side processing · files never uploaded</span>
              </li>
              <li className="flex items-center gap-2">
                <Shield className="h-3.5 w-3.5 text-[hsl(var(--color-success))] flex-shrink-0" aria-hidden="true" />
                <span>GDPR compliant · 100% private</span>
              </li>
            </ul>

            <div className="flex gap-2">
              <a
                href="https://github.com/ShuttleLab/pdf-shuttle"
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 rounded-full bg-[hsl(var(--color-muted))] text-[hsl(var(--color-muted-foreground))] hover:bg-[hsl(var(--color-primary))] hover:text-white transition-all"
                aria-label="GitHub repository"
              >
                <Github className="w-4 h-4" />
              </a>
              <a
                href="mailto:support@shuttlelab.org"
                className="p-2 rounded-full bg-[hsl(var(--color-muted))] text-[hsl(var(--color-muted-foreground))] hover:bg-[hsl(var(--color-primary))] hover:text-white transition-all"
                aria-label="Email support"
              >
                <Mail className="w-4 h-4" />
              </a>
            </div>
          </div>

          {/* Column 2: Resources */}
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider text-[hsl(var(--color-foreground))] mb-5">
              {t('footer.resources') || 'Resources'}
            </h3>
            <ul className="flex flex-col gap-3">
              {resourceLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-primary))] transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3: Other ShuttleLab Tools (cross-promotion) */}
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider text-[hsl(var(--color-foreground))] mb-5">
              {t('footer.otherTools') || 'Other ShuttleLab Tools'}
            </h3>
            <ul className="flex flex-col gap-3">
              {SHUTTLELAB_PRODUCTS.map((product) => (
                <li key={product.href}>
                  <a
                    href={product.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group flex items-start gap-2 text-sm text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-foreground))] transition-colors"
                  >
                    <span className="text-base leading-none" aria-hidden="true">{product.emoji}</span>
                    <span className="flex flex-col gap-0.5">
                      <span className="font-medium group-hover:text-[hsl(var(--color-primary))] transition-colors">
                        {product.name}
                      </span>
                      <span className="text-xs text-[hsl(var(--color-muted-foreground))/0.8]">
                        {product.desc}
                      </span>
                    </span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Copyright + source code attribution (AGPL §13 compliance) */}
        <div className="pt-8 border-t border-[hsl(var(--color-border))] flex flex-col md:flex-row items-center justify-between gap-3">
          <div className="flex flex-col gap-1 text-center md:text-left">
            <p className="text-sm text-[hsl(var(--color-muted-foreground))]">
              &copy; {currentYear} ShuttleLab. All rights reserved.
            </p>
            <p className="text-xs text-[hsl(var(--color-muted-foreground))/0.7]">
              <a
                href="https://github.com/ShuttleLab/pdf-shuttle"
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:text-[hsl(var(--color-foreground))]"
              >
                Source code
              </a>{' '}
              (AGPL-3.0) · Based on{' '}
              <a
                href="https://github.com/PDFCraftTool/pdfcraft"
                target="_blank"
                rel="noopener noreferrer"
                className="underline hover:text-[hsl(var(--color-foreground))]"
              >
                PDFCraft
              </a>
            </p>
          </div>
          <div className="flex items-center gap-5 text-xs">
            <Link
              href={`/${locale}/about`}
              className="text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-foreground))]"
            >
              About
            </Link>
            <Link
              href={`/${locale}/privacy`}
              className="text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-foreground))]"
            >
              Privacy
            </Link>
            <Link
              href={`/${locale}/terms`}
              className="text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-foreground))]"
            >
              Terms
            </Link>
            <a
              href="mailto:support@shuttlelab.org"
              className="text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-foreground))]"
            >
              Contact
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
