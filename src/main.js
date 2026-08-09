// ── Vietnam Trip Planner — UI logic ───────────────────────────────────────
import { CITIES, INTERESTS, DURATIONS, BUDGETS, pickRoute, buildItinerary, transportOptions } from './data.js';
import './style.css';

const $ = (s) => document.querySelector(s);

const state = {
  duration: null,   // key in DURATIONS
  interests: [],    // keys in INTERESTS
  budget: 'mid',
  step: 1,
};

// ── Step renderers ─────────────────────────────────────────────────────────
function optCard(key, label, sub = '') {
  const d = document.createElement('button');
  d.className = 'opt';
  d.dataset.key = key;
  d.innerHTML = `<span class="opt-label">${label}</span>${sub ? `<span class="opt-sub">${sub}</span>` : ''}`;
  return d;
}

function renderDuration() {
  const box = $('#dur-opts'); box.innerHTML = '';
  for (const [k, v] of Object.entries(DURATIONS)) {
    const b = optCard(k, v.label, v.hint);
    b.addEventListener('click', () => { state.duration = k; selectIn(box, b); $('#btn-next').hidden = false; });
    box.append(b);
  }
}
function renderInterests() {
  const box = $('#int-opts'); box.innerHTML = '';
  for (const [k, v] of Object.entries(INTERESTS)) {
    const b = optCard(k, `${v.emoji} ${v.label}`);
    b.addEventListener('click', () => {
      const on = b.classList.toggle('selected');
      // toggle on/off multi-select
      state.interests = [...box.querySelectorAll('.selected')].map((x) => x.dataset.key);
      $('#btn-next').hidden = state.interests.length === 0;
    });
    box.append(b);
  }
}
function renderBudget() {
  const box = $('#bud-opts'); box.innerHTML = '';
  for (const [k, v] of Object.entries(BUDGETS)) {
    const b = optCard(k, v.label, k === 'budget' ? 'Hostels & street food' : k === 'mid' ? 'Comfortable 3★ + mix' : 'Boutique stays & fine dining');
    b.addEventListener('click', () => { state.budget = k; selectIn(box, b); $('#btn-generate').hidden = false; });
    box.append(b);
  }
}

function selectIn(box, el) { box.querySelectorAll('.opt').forEach((o) => o.classList.remove('selected')); el.classList.add('selected'); }

function showStep(n) {
  state.step = n;
  document.querySelectorAll('.planner-step').forEach((s) => (s.hidden = s.dataset.step != n));
  $('#btn-back').hidden = n === 1;
  $('#btn-next').hidden = !(n === 1 ? state.duration : n === 2 ? state.interests.length : false);
  $('#btn-generate').hidden = !(n === 3 && state.budget);
}
window.showStep = showStep;      // inline onclick (remote-click safety)
window.renderResults = renderResults;

// ── Results ────────────────────────────────────────────────────────────────
function renderResults() {
  const days = DURATIONS[state.duration].days;
  const route = pickRoute(state.interests, days);
  const plan = buildItinerary(route, state.interests, days, state.budget);
  const tOpts = transportOptions(route);
  const dist = plan.route.reduce((a, r) => a + (r.dist || 0), 0);

  $('#res-title').textContent = `Your ${DURATIONS[state.duration].label} Vietnam itinerary`;
  $('#res-sub').textContent = `${route.map((r) => CITIES[r].name).join(' → ')} · ~${Math.round(dist)} km covered · ${BUDGETS[state.budget].label} budget`;

  // route strip
  const strip = $('#route-strip'); strip.innerHTML = '';
  route.forEach((r, i) => {
    strip.insertAdjacentHTML('beforeend', `<span class="route-node">${CITIES[r].name}</span>`);
    if (i < route.length - 1) strip.insertAdjacentHTML('beforeend', `<span class="route-arrow">→</span>`);
  });

  // itinerary days
  const it = $('#itinerary'); it.innerHTML = '';
  let cur = null;
  plan.picked.forEach((p) => {
    if (cur !== p.day) {
      cur = p.day;
      it.insertAdjacentHTML('beforeend', `<div class="day-head">Day ${p.day}</div>`);
    }
    it.insertAdjacentHTML('beforeend',
      `<div class="it-item"><span class="it-emoji">${p.emoji || '📍'}</span><div><div class="it-title">${p.title}</div>` +
      `<div class="it-meta">${p.note}${p.hours ? ' · ' + p.hours + 'h' : ''}${p.cost ? ' · $' + p.cost : ''}</div></div></div>`);
  });

  // transport
  const tr = $('#transport'); tr.innerHTML = '';
  tOpts.forEach((t) => {
    tr.insertAdjacentHTML('beforeend',
      `<div class="tr-item"><span class="tr-mode">${t.mode}</span><div><div class="tr-title">${t.from} → ${t.to}</div><div class="tr-meta">~${t.time} hours · from $${t.price}</div></div></div>`);
  });
  tr.insertAdjacentHTML('beforeend', `<div class="tr-total">Total transport: <strong>~$${Math.round(plan.summary.transport)}</strong></div>`);

  // costs
  const c = plan.summary;
  const row = (k, v) => `<div class="cost-row"><span>${k}</span><strong>$${Math.round(v)}</strong></div>`;
  $('#costs').innerHTML = row('🏨 Accommodation', c.stay) + row('🍜 Food & drinks', c.food) +
    row('🎟️ Activities', c.sight) + row('🚌 Transport', c.transport) +
    `<div class="cost-total">${row('Total estimate', c.total)}</div>`;

  $('#results').hidden = false;
  $('#results').scrollIntoView({ behavior: 'smooth' });
}

// ── Regions grid ───────────────────────────────────────────────────────────
function renderRegions() {
  const grid = $('#regions-grid'); grid.innerHTML = '';
  const emo = { hanoi: '🎯', halong: '⛵', ninhbinh: '⛰️', sapa: '🏔️', hue: '🎎', danang: '🌊', hoi_an: '🏮' };
  for (const [k, c] of Object.entries(CITIES)) {
    grid.insertAdjacentHTML('beforeend',
      `<div class="region-card"><div class="region-emoji">${emo[k]}</div><h3>${c.name}</h3><p>${c.tagline}</p>` +
      `<div class="region-tags">${c.tags.map((t) => `<span>${INTERESTS[t].emoji}</span>`).join('')}</div></div>`);
  }
}

// ── Wire up ────────────────────────────────────────────────────────────────
renderDuration(); renderInterests(); renderBudget(); renderRegions();
$('#btn-next').addEventListener('click', () => showStep(state.step + 1));
$('#btn-back').addEventListener('click', () => showStep(state.step - 1));
$('#btn-generate').addEventListener('click', renderResults);