import '@testing-library/dom';
import '@testing-library/jest-dom/vitest';
import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import enMessages from '../../messages/en.json';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock next-intl so tests can call useTranslations without NextIntlClientProvider
vi.mock('next-intl', async (importOriginal) => {
  const actual: any = await importOriginal();
  function lookup(path: string): string {
    const parts = path.split('.');
    let current: any = enMessages;
    for (const p of parts) {
      if (current && typeof current === 'object' && p in current) current = current[p];
      else return path;
    }
    return typeof current === 'string' ? current : path;
  }
  return {
    ...actual,
    useTranslations: (namespace?: string) => {
      const t = (key: string, values?: Record<string, any>) => {
        const path = namespace ? `${namespace}.${key}` : key;
        let result = lookup(path);
        if (values) for (const k in values) result = result.replace(new RegExp(`\\{${k}\\}`, 'g'), String(values[k]));
        return result;
      };
      (t as any).rich = (key: string) => lookup(namespace ? `${namespace}.${key}` : key);
      (t as any).has = (_key: string) => true;
      return t;
    },
    useLocale: () => 'en',
    useFormatter: () => ({ dateTime: (d: Date) => d.toISOString(), number: (n: number) => String(n) }),
  };
});

// Mock next/navigation hooks for components like Header that use useRouter
vi.mock('next/navigation', async (importOriginal) => {
  const actual: any = await importOriginal();
  return {
    ...actual,
    useRouter: () => ({
      push: vi.fn(),
      replace: vi.fn(),
      refresh: vi.fn(),
      back: vi.fn(),
      forward: vi.fn(),
      prefetch: vi.fn(),
    }),
    usePathname: () => '/',
    useSearchParams: () => new URLSearchParams(),
    useParams: () => ({ locale: 'en' }),
  };
});

// Mock URL.createObjectURL and URL.revokeObjectURL for jsdom
if (typeof URL.createObjectURL === 'undefined') {
  URL.createObjectURL = vi.fn(() => 'blob:mock-url');
}
if (typeof URL.revokeObjectURL === 'undefined') {
  URL.revokeObjectURL = vi.fn();
}

// Mock window.matchMedia for responsive tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
class MockIntersectionObserver {
  observe = vi.fn();
  disconnect = vi.fn();
  unobserve = vi.fn();
}

Object.defineProperty(window, 'IntersectionObserver', {
  writable: true,
  value: MockIntersectionObserver,
});

// Mock ResizeObserver
class MockResizeObserver {
  observe = vi.fn();
  disconnect = vi.fn();
  unobserve = vi.fn();
}

Object.defineProperty(window, 'ResizeObserver', {
  writable: true,
  value: MockResizeObserver,
});
