// ── Vietnam Trip Planner — region photos (self-hosted, local files) ────────
// Imported via Vite so they get copied to dist/assets with hashed names
// (always served by GH Pages, no hotlink/rate-limit issues).
import hanoi from './assets/regions/hanoi.jpg';
import halong from './assets/regions/halong.jpg';
import ninhbinh from './assets/regions/ninhbinh.jpg';
import sapa from './assets/regions/sapa.jpg';
import hue from './assets/regions/hue.jpg';
import danang from './assets/regions/danang.jpg';
import hoian from './assets/regions/hoian.jpg';

export const REGION_IMAGES = {
  hanoi,
  halong,
  ninhbinh,
  sapa,
  hue,
  danang,
  hoi_an: hoian,
};