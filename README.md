# 🇻🇳 Vietnam Trip Planner

A static, single-page trip planner for Vietnam. Answer three questions — **how long** you're staying, **what you love** doing, and **how you like to travel** — and it builds a personalized itinerary: day-by-day plan, transport legs between cities, and a cost estimate.

Live: **[vietanh210304.github.io/vietnam-trip-planner](https://vietanh210304.github.io/vietnam-trip-planner)**

## Features

- **3 trip lengths** — a few days (3–4), one week (7), or a month (30)
- **6 interest tags** — nature, beach, culture, food, adventure, city life
- **3 budgets** — budget / mid-range / premium (cost multipliers)
- **7 handcrafted regions** — Hà Nội, Hạ Long, Ninh Bình, Sa Pa, Huế, Đà Nẵng, Hội An
- **Itinerary engine** — picks a route that fits your days, then schedules activities (morning/afternoon/evening + full-day items)
- **Transport legs** — real-ish bus/train/sleeper options between cities
- **Cost breakdown** — accommodation, food, activities, transport, total

## Tech stack

- Vanilla JS (no framework) + Vite
- Pure data/engine in `src/data.js` (dependency-free, unit-tested)
- Deployed via GitHub Actions → GitHub Pages

## Development

```bash
npm install
npm run dev       # local dev server
npm run build     # production build → dist/
npm test          # engine sanity checks (node test/engine.test.mjs)
npm run preview   # preview the build
```

## Project structure

```
src/
  index.html     # single page layout
  main.js        # UI wiring (step flow, results render)
  data.js        # cities, activities, transport, itinerary engine
  style.css      # dark, gradient-heavy theme
test/
  engine.test.mjs
.github/workflows/deploy.yml
```

Prices are rough estimates in USD — a demo of the *idea*, not a booking engine.

MIT © 2026