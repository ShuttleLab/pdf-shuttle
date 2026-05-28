'use client';

import React, { useEffect, useState } from 'react';
import { Sun, Moon, Monitor } from 'lucide-react';

type Theme = 'system' | 'light' | 'dark';

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>('system');
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem('theme') as Theme | null;
    if (savedTheme === 'light' || savedTheme === 'dark' || savedTheme === 'system') {
      setTheme(savedTheme);
    }

    // Check initial resolved theme
    const isDark = document.documentElement.classList.contains('dark');
    setResolvedTheme(isDark ? 'dark' : 'light');
  }, []);

  useEffect(() => {
    const applyTheme = () => {
      let isDark: boolean;
      
      if (theme === 'system') {
        isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      } else {
        isDark = theme === 'dark';
      }

      document.documentElement.classList.toggle('dark', isDark);
      setResolvedTheme(isDark ? 'dark' : 'light');
    };

    applyTheme();

    // Listen for system theme changes when in system mode
    if (theme === 'system') {
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      const handler = () => applyTheme();
      mq.addEventListener('change', handler);
      return () => mq.removeEventListener('change', handler);
    }
  }, [theme]);

  const cycleTheme = () => {
    const nextTheme: Theme = theme === 'system' ? 'light' : theme === 'light' ? 'dark' : 'system';
    setTheme(nextTheme);
    localStorage.setItem('theme', nextTheme);
  };

  // Render placeholder before hydrated to avoid mismatch
  if (theme === null) {
    return <div className="h-9 w-9" aria-hidden="true" />;
  }

  const getIcon = () => {
    switch (theme) {
      case 'system':
        return <Monitor className="h-5 w-5" aria-hidden="true" />;
      case 'light':
        return <Sun className="h-5 w-5" aria-hidden="true" />;
      case 'dark':
        return <Moon className="h-5 w-5" aria-hidden="true" />;
    }
  };

  const getLabel = () => {
    switch (theme) {
      case 'system':
        return 'System theme (follows OS)';
      case 'light':
        return 'Light mode';
      case 'dark':
        return 'Dark mode';
    }
  };

  return (
    <button
      onClick={cycleTheme}
      className="flex items-center justify-center h-9 w-9 rounded-lg text-[hsl(var(--color-muted-foreground))] hover:text-[hsl(var(--color-foreground))] hover:bg-[hsl(var(--color-muted))/0.5] transition-all"
      aria-label={getLabel()}
      title={getLabel()}
    >
      {getIcon()}
    </button>
  );
}
