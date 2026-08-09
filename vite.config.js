import { defineConfig } from 'vite';

export default defineConfig({
  root: 'src',
  base: '/vietnam-trip-planner/',
  build: { outDir: '../dist', emptyOutDir: true },
});