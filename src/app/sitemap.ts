/**
 * Sitemap Generation
 * Generates sitemap.xml for all pages across all locales
 * 
 * @see https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
 */

import { MetadataRoute } from 'next';
import { siteConfig } from '@/config/site';
import { locales, type Locale } from '@/lib/i18n/config';
import { getAllTools } from '@/config/tools';

export const dynamic = 'force-static';

/**
 * Core tool slugs — only these appear in sitemap.
 * Slim sitemap signals quality over quantity and avoids
 * the "template-site" perception from 90×13 near-identical tool pages.
 */
const CORE_TOOL_SLUGS = new Set([
  'merge-pdf',
  'split-pdf',
  'compress-pdf',
  'edit-pdf',
  'pdf-to-docx',
  'pdf-to-jpg',
  'jpg-to-pdf',
  'ocr-pdf',
  'sign-pdf',
  'encrypt-pdf',
  'extract-pages',
  'pdf-to-excel',
]);

/**
 * Priority values for different page types
 */
const PRIORITY = {
  home: 1.0,
  tools: 0.9,
  toolPage: 0.8,
  static: 0.6,
} as const;

/**
 * Change frequency for different page types
 */
const CHANGE_FREQUENCY = {
  home: 'daily',
  tools: 'weekly',
  toolPage: 'weekly',
  static: 'monthly',
} as const;

/**
 * Static pages that exist for all locales
 */
const STATIC_PAGES = [
  { path: '', priority: PRIORITY.home, changeFrequency: CHANGE_FREQUENCY.home },
  { path: '/tools', priority: PRIORITY.tools, changeFrequency: CHANGE_FREQUENCY.tools },
  { path: '/about', priority: PRIORITY.static, changeFrequency: CHANGE_FREQUENCY.static },
  { path: '/faq', priority: PRIORITY.static, changeFrequency: CHANGE_FREQUENCY.static },
  { path: '/privacy', priority: PRIORITY.static, changeFrequency: CHANGE_FREQUENCY.static },
  { path: '/contact', priority: PRIORITY.static, changeFrequency: CHANGE_FREQUENCY.static },
];

/**
 * Generate sitemap entries for a specific locale
 */
function generateLocaleEntries(locale: Locale, lastModified: Date): MetadataRoute.Sitemap {
  const entries: MetadataRoute.Sitemap = [];
  
  // Add static pages
  for (const page of STATIC_PAGES) {
    entries.push({
      url: `${siteConfig.url}/${locale}${page.path}`,
      lastModified,
      changeFrequency: page.changeFrequency as 'daily' | 'weekly' | 'monthly',
      priority: page.priority,
    });
  }
  
  // Add core tool pages only (not the full 90-tool catalogue)
  const tools = getAllTools().filter((t) => CORE_TOOL_SLUGS.has(t.slug));
  for (const tool of tools) {
    entries.push({
      url: `${siteConfig.url}/${locale}/tools/${tool.slug}`,
      lastModified,
      changeFrequency: CHANGE_FREQUENCY.toolPage,
      priority: PRIORITY.toolPage,
    });
  }
  
  return entries;
}

/**
 * Generate the complete sitemap
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  const allEntries: MetadataRoute.Sitemap = [];
  
  // Generate entries for each locale
  for (const locale of locales) {
    const localeEntries = generateLocaleEntries(locale, lastModified);
    allEntries.push(...localeEntries);
  }
  
  return allEntries;
}

/**
 * Get total number of URLs in sitemap
 * Useful for testing and validation
 */
export function getSitemapUrlCount(): number {
  const tools = getAllTools();
  const staticPagesCount = STATIC_PAGES.length;
  const toolPagesCount = tools.length;
  const localesCount = locales.length;
  
  return (staticPagesCount + toolPagesCount) * localesCount;
}
