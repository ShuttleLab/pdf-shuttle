/**
 * Font Configuration
 * Uses Geist font family (Vercel's font)
 * 
 * Uses next/font for automatic font optimization including:
 * - Font subsetting (only loads characters used)
 * - Self-hosting (no external requests to Google Fonts)
 * - Zero layout shift with size-adjust
 * - display: swap for better performance
 */

import { Geist, Geist_Mono } from 'next/font/google';

/**
 * Geist font - Primary sans-serif font
 * Used for body text and UI elements
 */
export const geistSans = Geist({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-geist-sans',
  preload: true,
  fallback: ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
  adjustFontFallback: true,
});

/**
 * Geist Mono font - Monospace font
 * Used for code snippets and technical content
 */
export const geistMono = Geist_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-geist-mono',
  preload: false,
  fallback: ['Fira Code', 'Consolas', 'Monaco', 'monospace'],
  adjustFontFallback: true,
});

/**
 * Combined font variables for use in className
 */
export const fontVariables = `${geistSans.variable} ${geistMono.variable}`;

/**
 * Font class names for direct usage
 */
export const fontClassNames = {
  sans: geistSans.className,
  mono: geistMono.className,
};

/**
 * CSS custom properties for fonts
 * These are set as CSS variables and can be used in Tailwind
 */
export const fontCssVariables = {
  '--font-sans': geistSans.style.fontFamily,
  '--font-mono': geistMono.style.fontFamily,
} as const;
