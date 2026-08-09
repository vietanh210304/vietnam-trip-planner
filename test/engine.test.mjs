#!/usr/bin/env node
// Engine sanity check — run: node test/engine.test.mjs
import { pickRoute, buildItinerary, DURATIONS } from '../src/data.js';

const cases = [
  ['fewdays', ['nature', 'food'], 'mid'],
  ['week', ['beach', 'culture'], 'mid'],
  ['month', ['food', 'city', 'culture'], 'luxury'],
  ['week', ['adventure'], 'budget'],
  ['fewdays', ['beach'], 'mid'],
  ['month', ['nature'], 'luxury'],
  ['week', ['city'], 'mid'],
];
let fail = 0;
for (const [d, ints, b] of cases) {
  const route = pickRoute(ints, DURATIONS[d].days);
  const plan = buildItinerary(route, ints, DURATIONS[d].days, b);
  const t = plan.summary.total;
  const ok = Number.isFinite(t) && t > 0 && plan.picked.length > 0;
  if (!ok) fail++;
  console.log(`${ok ? '✓' : '✗'} ${d} ${ints.join('+')} → ${route.join(' → ')} | $${Math.round(t)}`);
}
process.exit(fail ? 1 : 0);