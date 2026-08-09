// ── Vietnam Trip Planner — trip data & itinerary engine ──────────────────
// Pure data + pure functions; no DOM. Kept dependency-free on purpose.

// Priority-tagged activity pools per city. Tags: nature, culture, food, beach, adventure, city, history
export const CITIES = {
  hanoi: {
    name: 'Hà Nội', tagline: 'Old Quarter charm · lakes · history',
    tags: ['culture', 'history', 'food', 'city'],
    day: 1.5,        // base days to "do" this city
    costs: { stay: 25, food: 15, sight: 12, inout: { budget: 35, mid: 70 } },
    to: {
      halong: { time: 3, price: 14, mode: '🚌 Bus' },
      ninhbinh: { time: 2.5, price: 10, mode: '🚌 Bus' },
      sapa: { time: 9, price: 32, mode: '🚆 Sleeper train' },
    },
    activities: [
      // [tag, title, duration_hours, cost, {needFullDay}]
      ['culture', 'Hanoi Old Quarter & Hoan Kiem Lake walk', 3, 5, {}],
      ['history', 'Ho Chi Minh Mausoleum & One Pillar Pagoda', 3, 0, {}],
      ['culture', 'Temple of Literature — Vietnam\'s first university', 2.5, 3, {}],
      ['food', 'Egg coffee & street food tour (Train Street)', 2.5, 10, {}],
      ['culture', 'Water Puppet Theatre show', 1.5, 10, {}],
      ['city', 'West Lake / Tran Quoc Pagoda sunset', 2, 0, {}, {fitsAnywhere: true}],
      ['food', 'Night market food crawl (weekend)', 3, 12, {weekend: true}],
      ['nature', 'Bat Trang pottery village day trip', 8, 15, {needFullDay: true}],
    ],
  },
  halong: {
    name: 'Hạ Long', tagline: 'Emerald bay · limestone karsts · cruises',
    tags: ['nature', 'beach', 'adventure'],
    day: 1.5,
    costs: { stay: 45, food: 18, sight: 25, inout: { budget: 35, mid: 70 } },
    to: { ninhbinh: { time: 3, price: 15, mode: '🚌 Bus' } },
    activities: [
      ['nature', 'Day cruise among the karsts (Ti Top island)', 8, 35, {needFullDay: true}],
      ['adventure', 'Sunset cruise on the bay', 3, 25, {}],
      ['beach', 'Bai Chay beach & promenade', 2, 0, {}],
      ['nature', 'Sung Sot Cave (Surprise Cave)', 2.5, 20, {needFullDay: true}],
      ['food', 'Seafood dinner at Cai Dam market', 2, 15, {}],
    ],
  },
  ninhbinh: {
    name: 'Ninh Bình', tagline: 'Halong-on-land · rice paddies · caves',
    tags: ['nature', 'adventure', 'history'],
    day: 1.5,
    costs: { stay: 20, food: 12, sight: 15, inout: { budget: 25, mid: 50 } },
    to: {
      hue: { time: 12, price: 26, mode: '🚆 Sleeper train' },
      sapa: { time: 10, price: 35, mode: '🚆 Sleeper train' },
    },
    activities: [
      ['nature', 'Trang An boat trip (caves & temples)', 4, 25, {needFullDay: true}],
      ['adventure', 'Mua Cave viewpoint — 500 steps', 2.5, 7, {}],
      ['history', 'Hoa Lu ancient capital temples', 2.5, 5, {}],
      ['nature', 'Tam Coc river rowing (less crowded)', 4, 25, {needFullDay: true}],
      ['food', 'Mountain goat + rice wine dinner', 2, 12, {}],
    ],
  },
  sapa: {
    name: 'Sa Pa', tagline: 'Terraced rice fields · Fansipan · hill tribes',
    tags: ['nature', 'adventure'],
    day: 2.5,
    costs: { stay: 25, food: 14, sight: 20, inout: { budget: 30, mid: 60 } },
    to: { ninhbinh: { time: 10, price: 35, mode: '🚆 Sleeper train' } },
    activities: [
      ['nature', 'Cat Cat village trek (Hmong culture)', 4, 10, {}],
      ['adventure', 'Fansipan cable car — roof of Indochina', 6, 28, {needFullDay: true}],
      ['nature', 'Terraced rice field trek to Lao Chai–Ta Van', 6, 15, {needFullDay: true}],
      ['adventure', 'Sunrise at Ham Rong viewpoint', 3, 5, {}],
      ['food', 'Grilled skewers & local corn wine', 2, 8, {}],
    ],
  },
  hue: {
    name: 'Huế', tagline: 'Imperial city · royal tombs · riverside',
    tags: ['history', 'culture', 'food'],
    day: 2,
    costs: { stay: 22, food: 13, sight: 18, inout: { budget: 30, mid: 60 } },
    to: {
      danang: { time: 3, price: 12, mode: '🚌 Bus' },
      hoi_an: { time: 3.5, price: 14, mode: '🚌 Bus' },
    },
    activities: [
      ['history', 'Imperial Citadel & Forbidden City', 4, 12, {needFullDay: true}],
      ['history', 'Royal tombs of Khai Dinh & Minh Mang', 4, 10, {needFullDay: true}],
      ['food', 'Bun Bo Hue & banh khoai food tour', 2.5, 10, {}],
      ['culture', 'Perfume River boat ride — Thien Mu pagoda', 3, 8, {}],
      ['history', 'Dong Ba market & royal cake tasting', 2, 5, {}],
    ],
  },
  danang: {
    name: 'Đà Nẵng', tagline: 'Beach city · bridges · Marble Mountains',
    tags: ['beach', 'city', 'food', 'adventure'],
    day: 2,
    costs: { stay: 28, food: 15, sight: 15, inout: { budget: 30, mid: 60 } },
    to: { hoi_an: { time: 1, price: 5, mode: '🚌 Shuttle' } },
    activities: [
      ['city', 'My Khe beach day (swim + seafood lunch)', 5, 5, {needFullDay: true}],
      ['adventure', 'Son Tra Peninsula — Monkey Mountain drive', 3, 10, {}],
      ['beach', 'Marble Mountains caves & temples', 3, 8, {}],
      ['city', 'Dragon Bridge fire show (Fri–Sun 9pm)', 1.5, 0, {weekend: true}],
      ['city', 'Ba Na Hills — Golden Bridge (full day)', 8, 55, {needFullDay: true}],
      ['food', 'Mi Quang & banh xeo street dinner', 2, 8, {}],
    ],
  },
  hoi_an: {
    name: 'Hội An', tagline: 'Lantern town · tailors · ancient alleys',
    tags: ['culture', 'food', 'city', 'beach'],
    day: 1.5,
    costs: { stay: 26, food: 14, sight: 12, inout: { budget: 25, mid: 50 } },
    to: {
      danang: { time: 1, price: 5, mode: '🚌 Shuttle' },
      hue: { time: 3.5, price: 14, mode: '🚌 Bus' },
    },
    activities: [
      ['culture', 'Ancient Town lantern walk at dusk', 3, 0, {}],
      ['culture', 'Japanese Covered Bridge & old houses', 2.5, 6, {}],
      ['food', 'Cao Lau & white rose dumplings food tour', 2, 10, {}],
      ['beach', 'An Bang beach bike ride', 3, 3, {}],
      ['city', 'Tailor-made clothing (ao dai / suit)', 4, 30, {}, {fitsAnywhere: true}],
      ['nature', 'Tra Que vegetable village cooking class', 4, 20, {}],
    ],
  },
};

export const INTERESTS = {
  nature:    { label: 'Nature & landscape', emoji: '🏔️' },
  beach:     { label: 'Beach & relax', emoji: '🏖️' },
  culture:   { label: 'History & culture', emoji: '🏛️' },
  food:      { label: 'Foodie', emoji: '🍜' },
  adventure: { label: 'Adventure', emoji: '🧗' },
  city:      { label: 'City life', emoji: '🌆' },
};

export const DURATIONS = {
  fewdays: { label: 'A few days (3–4)', days: 3.5, hint: 'Classic North or Central loop' },
  week:    { label: 'One week (7)', days: 7, hint: 'Two regions, comfortable pace' },
  month:   { label: 'A month (30)', days: 30, hint: 'North → Central → South, slow travel' },
};

export const BUDGETS = {
  budget: { label: 'Budget', mult: 1 },
  mid:    { label: 'Mid-range', mult: 1.6 },
  luxury: { label: 'Premium', mult: 2.6 },
};

// ── Itinerary engine ──────────────────────────────────────────────────────

// ROUGH straight-line distance between centers (km) for "how far you can go".
const KM = {
  'hanoi-halong': 160, 'hanoi-ninhbinh': 110, 'hanoi-sapa': 320,
  'halong-ninhbinh': 170,
  'ninhbinh-hue': 550, 'ninhbinh-sapa': 400,
  'sapa-ninhbinh': 400,
  'hue-danang': 100, 'hue-hoi_an': 115,
  'danang-hoi_an': 40,
};
const key = (a, b) => `${a}-${b}`;

export function pickRoute(interests = ['nature', 'food'], days = 7) {
  const score = (city) => {
    const t = CITIES[city].tags;
    const hits = interests.filter((i) => t.includes(i)).length;
    return hits + (t.length / 10); // tie-break: more versatile city edges ahead
  };
  const ranked = Object.keys(CITIES).sort((a, b) => score(b) - score(a));
  const totalDays = CITIES[ranked[0]].day + CITIES[ranked[1]].day + 1; // +1 travel
  // Too far for the trip? contract to the top 2 best-scoring cities that fit.
  if (totalDays > days) {
    for (let i = ranked.length - 1; i >= 0; i--) {
      const combo = CITIES[ranked[0]].day + CITIES[ranked[i]].day + 1;
      if (combo <= days && i >= 1) return ranked.slice(0, 1).concat([ranked[i]]);
    }
    return ranked.slice(0, 1);
  }
  // Enough time? stretch to 3 cities when it fits
  if (days >= 8 && ranked.length >= 3) {
    const trio = CITIES[ranked[0]].day + CITIES[ranked[1]].day + CITIES[ranked[2]].day + 2;
    if (trio <= days) return ranked.slice(0, 3);
  }
  return ranked.slice(0, 2);
}

export function routeDistance(cities) {
  let km = 0;
  for (let i = 0; i < cities.length - 1; i++) {
    const k = key(cities[i], cities[i + 1]);
    km += KM[k] ?? 999;
  }
  return km;
}

export function buildItinerary(route, interests, days, budgetKey = 'mid') {
  const mult = BUDGETS[budgetKey].mult;
  const picked = [];       // [{day, city, title, cost, emoji}]
  const perCity = {};
  let day = 1;

  route.forEach((cityKey, idx) => {
    const city = CITIES[cityKey];
    const acts = city.activities.slice().sort((a, b) => {
      // interest-matched first, then full-day activities sink to whole days
      const match = (x) => (interests.some((i) => x[0] === i) ? -1 : 0);
      return match(a) - match(b);
    });
    perCity[cityKey] = Math.max(2, Math.min(4, Math.round(city.day / 2) + 1));
    let remaining = Math.ceil(city.day); // full days in this city
    let slot = 1; // morning/afternoon/evening
    let used = 0;
    for (const a of acts) {
      if (used >= perCity[cityKey] || remaining <= 0) break;
      if (a[4] && a[4].needFullDay) {
        // consumes a whole day
        picked.push({ day, city: city.name, emoji: cityEmoji(cityKey), title: a[1], hours: a[2], cost: Math.round(a[3] * mult), note: 'Full day' });
        day += 1; remaining -= 1; used += 1; slot = 1;
        continue;
      }
      picked.push({ day, city: city.name, emoji: cityEmoji(cityKey), title: a[1], hours: a[2], cost: Math.round(a[3] * mult), note: slotName(slot) });
      slot = (slot % 3) + 1;
      used += 1;
      if (a[4] && a[4].weekend && slotBoundary()) break;
    }
    if (idx < route.length - 1 && city.to && city.to[route[idx + 1]]) {
      picked.push({ day, city: '', emoji: '🚌', title: `Travel to ${CITIES[route[idx + 1]].name}`, hours: 0, cost: Math.round(city.to[route[idx + 1]].price * mult), note: 'Transfer' });
      day += 1;
    }
  });

  // costs
  let stay = 0, food = 0, sight = 0, transport = 0;
  for (const cityKey of route) {
    const c = CITIES[cityKey];
    const d = Math.ceil(c.day);
    stay += c.costs.stay * d * mult;
    food += c.costs.food * d * mult;
    sight += c.costs.sight * d * mult;
  }
  for (let i = 0; i < route.length - 1; i++) {
    const leg = CITIES[route[i]].to && CITIES[route[i]].to[route[i + 1]];
    transport += (leg && leg.price ? leg.price : 30) * mult;
  }
  transport += (CITIES[route[0]].costs.inout[budgetKey] ?? CITIES[route[0]].costs.inout.mid) * mult; // arrive in/out
  const total = stay + food + sight + transport;

  return {
    route: route.map((r) => ({ key: r, ...CITIES[r], dist: routeDistance(route) })),
    days,
    budget: budgetKey,
    picked,
    summary: { stay, food, sight, transport, total, perCity },
    mult,
  };
}

function cityEmoji(key) {
  return { hanoi: '🎯', halong: '⛵', ninhbinh: '⛰️', sapa: '🏔️', hue: '🎎', danang: '🌊', hoi_an: '🏮' }[key] || '📍';
}
function slotName(n) { return ['Morning', 'Afternoon', 'Evening'][n - 1]; }
function slotBoundary() { return true; } // simple: weekend items always allowed in line

// ── Transport options (for a trip) ────────────────────────────────────────
export function transportOptions(route) {
  const out = [];
  for (let i = 0; i < route.length - 1; i++) {
    const from = route[i], to = route[i + 1];
    out.push({ from: CITIES[from].name, to: CITIES[to].name, ...CITIES[from].to[to] });
  }
  return out;
}