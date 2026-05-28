import { defineRouting } from 'next-intl/routing';
import { locales, defaultLocale } from '@/lib/i18n/config';

export const routing = defineRouting({
  // A list of all locales that are supported
  locales,

  // Used when no locale matches
  defaultLocale,

  // Use locale prefix only for non-default locales
  // Default locale (en) is at /, others at /zh/, /ja/, etc.
  localePrefix: 'as-needed',
});
