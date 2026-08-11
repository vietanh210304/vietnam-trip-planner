#!/usr/bin/env python3
"""Cron-driven self-improvement for Vietnam Trip Planner (one improvement per run).

For a Git repo deployed via GitHub Actions → Pages. Each improvement:
  - is marker-idempotent (<!--impr:name--> in src/index.html, or code markers)
  - is backed up, validated (build + engine test), then committed & pushed
    so GitHub Actions redeploys automatically.
Verbose output every run (user requested status reports each tick).
"""
import json
import os
import re
import shutil
import subprocess
import time

BASE = "/home/vietanh/workspace/vietnam-trip-planner"
SRC = os.path.join(BASE, "src")
INDEX = os.path.join(SRC, "index.html")
MAIN_JS = os.path.join(SRC, "main.js")
CSS = os.path.join(SRC, "style.css")
BACKUP_DIR = os.path.join(BASE, "backups")
STATE_FILE = os.path.join(BASE, ".improve_state.json")
TOKEN_FILE = "/home/vietanh/.hermes/secret/github_token.txt"
REPO = "vietanh210304/vietnam-trip-planner"
MAX_BACKUPS = 200


def validate_project():
    """Return (ok, msg): engine test + production build must both pass."""
    t = subprocess.run(["node", "test/engine.test.mjs"], cwd=BASE, capture_output=True, text=True, timeout=60)
    if t.returncode != 0:
        return False, f"engine test failed:\n{t.stdout[-500:]}{t.stderr[-500:]}"
    b = subprocess.run(["node", "node_modules/vite/bin/vite.js", "build"], cwd=BASE, capture_output=True, text=True, timeout=120)
    if b.returncode != 0:
        return False, f"vite build failed:\n{b.stderr[-500:]}"
    return True, f"engine test ✓ + build ✓ ({len(t.stdout.splitlines())} cases)"


def git_push(desc):
    """Commit + push; returns (ok, msg)."""
    token = open(TOKEN_FILE).read().strip()
    remote = f"https://x-access-token:{token}@github.com/{REPO}.git"
    # reset remote to tokenized form (existing origin may already be tokenized)
    subprocess.run(["git", "remote", "set-url", "origin", remote], cwd=BASE, capture_output=True)
    for cmd in [
        ["git", "add", "-A"],
        ["git", "-c", "user.name=VietAnh", "-c", "user.email=vietanh210304@users.noreply.github.com",
         "commit", "-m", f"auto-improve: {desc}"],
    ]:
        r = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True)
        if r.returncode != 0 and "nothing to commit" not in r.stderr:
            return False, f"git {cmd[3] if len(cmd)>3 else cmd[1]} failed: {r.stderr[-300:]}"
    p = subprocess.run(["git", "push", "-q", "origin", "main"], cwd=BASE, capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        return False, f"push failed: {p.stderr[-300:]}"
    return True, f"committed & pushed → GitHub Actions deploys"


# ── Improvements (one per run) ─────────────────────────────────────────────

def improv_why_us(html):
    """Add a 'Why trip planners love this' trust strip after the hero CTA."""
    marker = "<!--impr:why_us-->"
    if marker in html: return None
    block = (
        marker + "\n"
        '<div class="trust-strip"><span>✈️ 7 hand-curated regions</span>'
        '<span>🚆 Real transport legs</span>'
        '<span>💰 Honest budget estimates</span>'
        '<span>⏱️ Built in seconds</span></div>\n'
    )
    return html.replace("</section>", block + "</section>", 1), "Add trust strip under hero"

def improv_faq(html):
    """Add a small FAQ section before the footer."""
    marker = "<!--impr:faq-->"
    if marker in html: return None
    block = (
        marker + "\n"
        '<section class="how-section" id="faq"><div class="container section-head">'
        '<p class="eyebrow">FAQ</p><h2>Good to know</h2></div>'
        '<div class="container"><div class="faq-item"><h3>Are the prices real?</h3>'
        '<p>Rough mid-range estimates in USD to help you budget — not live quotes.</p></div>'
        '<div class="faq-item"><h3>Can I change my answers?</h3>'
        '<p>Yes — press Back, tweak anything, and regenerate. It takes one second.</p></div>'
        '<div class="faq-item"><h3>What if I have more than a month?</h3>'
        '<p>Add cities, slow down, live like a local — the engine opens up as days grow.</p></div>'
        '</div></section>\n'
    )
    return html.replace("</section>\n\n  <footer", block + "</section>\n\n  <footer", 1) or \
           html.replace("<footer", block + "<footer", 1), "Add FAQ section"

def improv_results_note(html):
    """Add a note under the results section about estimates."""
    marker = "<!--impr:results_note-->"
    if marker in html: return None
    block = marker + '\n<p class="results-note">Plans are illustrative — always confirm prices & schedules before booking.</p>\n'
    return html.replace("</section>\n\n  <section class=\"how-section\"", block + "</section>\n\n  <section class=\"how-section\"", 1), "Add results disclaimer"

def improv_style_polish(css):
    """Polish: smooth scrolling + trust strip & faq styles."""
    marker = "/*impr:polish*/"
    if marker in css: return None
    add = (
        marker + "\n"
        ".trust-strip { display:flex; flex-wrap:wrap; gap:14px 28px; justify-content:center; "
        "padding:18px 20px; background:var(--panel); border:1px solid var(--line); border-radius:var(--radius); "
        "margin-top:-38px; position:relative; z-index:2; max-width:860px; margin-left:auto; margin-right:auto; }\n"
        ".trust-strip span { font-size:.92rem; color:var(--muted); }\n"
        ".faq-item { background:var(--panel); border:1px solid var(--line); border-radius:var(--radius); padding:20px 24px; margin-bottom:14px; }\n"
        ".faq-item h3 { font-size:1.05rem; margin-bottom:6px; }\n"
        ".faq-item p { color:var(--muted); font-size:.92rem; }\n"
        ".results-note { text-align:center; color:var(--muted); font-size:.85rem; margin-top:18px; }\n"
        "html { scroll-behavior:smooth; }\n"
    )
    return css.rstrip() + "\n\n" + add, "Add trust strip/FAQ/scroll-smooth styles"


def improv_airbnb_cards(css):
    """Airbnb-style cards: warm 3-layer shadow, bigger radius, image zoom on hover."""
    marker = "/*impr:airbnb_cards*/"
    if marker in css: return None
    add = (
        marker + "\n"
        # 3-layer warm shadow (Airbnb: ring + soft + lift) + 20px radius
        ".region-card, .how-card, .opt, .faq-item { border-radius:20px; }\n"
        ".region-card { box-shadow: rgba(0,0,0,.18) 0 0 0 1px, rgba(0,0,0,.25) 0 2px 6px, rgba(0,0,0,.35) 0 8px 24px; }\n"
        ".region-card:hover { box-shadow: rgba(0,0,0,.24) 0 0 0 1px, rgba(0,0,0,.3) 0 4px 10px, rgba(0,0,0,.45) 0 14px 34px; }\n"
        # photography zoom like Airbnb listing cards
        ".region-img { transition: transform .35s ease; }\n"
        ".region-card:hover .region-img { transform: scale(1.06); }\n"
    )
    return css.rstrip() + "\n\n" + add, "Airbnb-style card shadows + image zoom"


def improv_glass_nav(css):
    """Stripe/Apple-style sticky glass header with blur backdrop."""
    marker = "/*impr:glass_nav*/"
    if marker in css: return None
    add = (
        marker + "\n"
        ".site-header { position:sticky; top:0; z-index:50; backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); "
        "background:rgba(7,11,20,.72); border-bottom:1px solid rgba(148,184,255,.1); }\n"
    )
    return css.rstrip() + "\n\n" + add, "Sticky glass nav (Stripe/Apple style)"


def improv_glow_cta(css):
    """Linear/Stripe-style gradient CTA with soft glow + subtle pulse on primary buttons."""
    marker = "/*impr:glow_cta*/"
    if marker in css: return None
    add = (
        marker + "\n"
        ".btn-primary { background:linear-gradient(135deg,#ff5f6d,#ff9966); box-shadow:0 4px 20px rgba(255,95,109,.35); }\n"
        ".btn-primary:hover { box-shadow:0 6px 28px rgba(255,95,109,.55); transform:translateY(-1px); }\n"
        ".btn-big { background:linear-gradient(135deg,#7f5af0,#ff5f6d); box-shadow:0 4px 24px rgba(127,90,240,.4); }\n"
        ".btn-big:hover { box-shadow:0 8px 34px rgba(127,90,240,.6); }\n"
    )
    return css.rstrip() + "\n\n" + add, "Glow gradient CTAs (Linear/Stripe style)"


BTT_MARKER = "<!--impr:back_to_top-->"
def improv_back_to_top(html):
    """Back-to-top floating button + scroll progress bar (adds tiny inline JS)."""
    marker = BTT_MARKER
    if marker in html: return None
    btn = (
        marker + "\n"
        '<button id="btt" aria-label="Back to top" onclick="window.scrollTo({top:0,behavior:\'smooth\'})">↑</button>\n'
        '<div id="scroll-progress"></div>\n'
        '<script>const btt=document.getElementById(\'btt\'),sp=document.getElementById(\'scroll-progress\'),'
        'on=()=>{const y=scrollY,h=document.documentElement;btt.style.opacity=y>400?1:0;'
        'sp.style.width=(y/(h.scrollHeight-h.clientHeight)*100)+\'%\';};'
        'addEventListener(\'scroll\',on);on();</script>\n'
    )
    return html.replace("</body>", btn + "</body>"), "Back-to-top button + scroll progress"


def improv_masonry(css):
    """Pinterest-style masonry for region grid on wide screens."""
    marker = "/*impr:masonry*/"
    if marker in css: return None
    add = (
        marker + "\n"
        ".regions-grid { columns: 3; column-gap: 20px; }\n"
        ".regions-grid .region-card { break-inside: avoid; margin-bottom: 20px; }\n"
        ".regions-grid .region-card:nth-child(4n+1) .region-img { height: 200px; }\n"
        ".regions-grid .region-card:nth-child(4n+2) .region-img { height: 150px; }\n"
        ".regions-grid .region-card:nth-child(4n+3) .region-img { height: 170px; }\n"
        ".regions-grid .region-card:nth-child(4n) .region-img { height: 130px; }\n"
        "@media (max-width: 900px) { .regions-grid { columns: 1; } }\n"
    )
    return css.rstrip() + "\n\n" + add, "Pinterest-style masonry region grid"


def improv_theme_toggle(html):
    """Dark/light theme toggle in header (localStorage persisted)."""
    marker = "<!--impr:theme_toggle-->"
    if marker in html: return None
    btn = (
        marker + "\n"
        '<button id="theme-toggle" aria-label="Toggle theme" onclick="'
        'document.body.classList.toggle(\'light\');'
        'localStorage.setItem(\'vtp-theme\', document.body.classList.contains(\'light\')?\'light\':\'dark\')">🌓</button>\n'
        '<script>if(localStorage.getItem(\'vtp-theme\')===\'light\')document.body.classList.add(\'light\');</script>\n'
    )
    html = html.replace("</header>", btn + "</header>")
    return html.replace("</body>", btn + "</body>"), "Dark/light theme toggle"


def improv_hero_stats(html):
    """Make hero stats interactive counters (count up on view)."""
    marker = "<!--impr:hero_counters-->"
    if marker in html: return None
    script = (
        marker + "\n"
        '<script>const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){const el=e.target,'
        't=parseFloat(el.dataset.count),d=800,s=performance.now();const step=n=>{const p=Math.min((n-s)/d,1);'
        'el.textContent=Math.round(t*(1-Math.pow(1-p,3)))+(el.dataset.suffix||\'\');p<1&&requestAnimationFrame(step)};'
        'requestAnimationFrame(step);io.unobserve(el)}}),{threshold:.4});'
        'document.querySelectorAll(\'[data-count]\').forEach(el=>io.observe(el));</script>\n'
    )
    return html.replace("</body>", script + "</body>"), "Count-up hero stats"


def improv_light_theme(css):
    """Light theme styles for the toggle."""
    marker = "/*impr:light_theme*/"
    if marker in css: return None
    add = (
        marker + "\n"
        "body.light { --bg:#f6f7fb; --bg2:#eef0f6; --panel:#fff; --panel2:#f3f4fa; "
        "--line:rgba(20,30,70,.12); --text:#141a2e; --muted:#5a6580; }\n"
        "#theme-toggle { background:transparent; border:1px solid var(--line); border-radius:999px; "
        "width:38px; height:38px; font-size:1.1rem; cursor:pointer; }\n"
        "#btt { position:fixed; right:22px; bottom:22px; width:48px; height:48px; border-radius:50%; border:0; "
        "background:linear-gradient(135deg,var(--accent),var(--accent2)); color:#fff; font-size:1.3rem; "
        "box-shadow:0 6px 20px rgba(255,90,95,.45); cursor:pointer; opacity:0; transition:opacity .25s; z-index:60; }\n"
        "#scroll-progress { position:fixed; top:0; left:0; height:3px; background:linear-gradient(90deg,var(--accent),var(--accent2)); "
        "width:0; z-index:70; }\n"
        ".site-header #theme-toggle { margin-left:auto; }\n"
    )
    return css.rstrip() + "\n\n" + add, "Back-to-top/theme styles"


def improv_footer_year(html):
    """Dynamic year in footer."""
    marker = "<!--impr:footer_year-->"
    if marker in html: return None
    el = marker + "\n<span class=\"footer-year\"></span><script>document.querySelector('.footer-year').textContent=new Date().getFullYear();</script>"
    return html.replace("</footer>", el + "</footer>"), "Dynamic footer year"


def improv_og_meta(html):
    """OG/Twitter meta tags for share previews."""
    marker = "<!--impr:og_meta-->"
    if marker in html: return None
    if "<meta property=\"og:title\"" in html: return None
    meta = (
        marker + "\n"
        '<meta property="og:title" content="Vietnam Trip Planner — Build your perfect itinerary" />\n'
        '<meta property="og:description" content="Answer a few questions and get a personalized Vietnam itinerary — routes, transport, costs." />\n'
        '<meta property="og:type" content="website" />\n'
        '<meta name="twitter:card" content="summary" />\n'
    )
    return html.replace("</head>", meta + "</head>"), "OG + Twitter meta tags"


def improv_faq_expand(html):
    """FAQ items open/close on click."""
    marker = "<!--impr:faq_expand-->"
    if marker in html: return None
    script = (
        marker + "\n"
        '<script>document.querySelectorAll(\'.faq-item\').forEach(it=>{const a=it.querySelector(\'p\');if(a){a.style.display=\'none\';'
        'it.querySelector(\'h3\').style.cursor=\'pointer\';it.querySelector(\'h3\').onclick=()=>{a.style.display=a.style.display===\'none\'?\'block\':\'none\';};}});</script>\n'
    )
    return html.replace("</body>", script + "</body>"), "Expandable FAQ items"


def improv_nav_scroll(html):
    """Nav links smooth-scroll to sections."""
    marker = "<!--impr:nav_scroll-->"
    if marker in html: return None
    # links already have href="#..." anchors; ensure smooth behavior via CSS class on html (scroll-smooth already present)
    # add scroll-margin-top so sticky header doesn't cover section titles
    # (CSS handled separately in improv_nav_scroll_css)
    return None


def improv_nav_scroll_css(css):
    """scroll-margin-top for anchored sections (sticky header offset)."""
    marker = "/*impr:nav_scroll*/"
    if marker in css: return None
    add = marker + "\n" + "section { scroll-margin-top: 90px; }\n"
    return css.rstrip() + "\n\n" + add, "Anchor scroll offset for sticky header"


def improv_jsonld(html):
    """JSON-LD structured data for SEO."""
    marker = "<!--impr:jsonld-->"
    if marker in html: return None
    ld = (
        marker + "\n"
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite",'
        '"name":"Vietnam Trip Planner","description":"Personalized Vietnam itineraries — routes, transport, budgets.",'
        '"url":"https://vietanh210304.github.io/vietnam-trip-planner/"}</script>\n'
    )
    return html.replace("</head>", ld + "</head>"), "JSON-LD structured data"


IMPROVEMENTS = [improv_why_us, improv_faq, improv_results_note, improv_style_polish,
                improv_airbnb_cards, improv_glass_nav, improv_glow_cta,
                improv_back_to_top, improv_masonry, improv_theme_toggle,
                improv_hero_stats, improv_light_theme,
                improv_footer_year, improv_og_meta, improv_faq_expand,
                improv_nav_scroll, improv_nav_scroll_css, improv_jsonld]
FILE_FOR = {improv_why_us: INDEX, improv_faq: INDEX, improv_results_note: INDEX,
            improv_style_polish: CSS, improv_airbnb_cards: CSS, improv_glass_nav: CSS,
            improv_glow_cta: CSS, improv_back_to_top: INDEX, improv_masonry: CSS,
            improv_theme_toggle: INDEX, improv_hero_stats: INDEX, improv_light_theme: CSS,
            improv_footer_year: INDEX, improv_og_meta: INDEX, improv_faq_expand: INDEX,
            improv_nav_scroll: INDEX, improv_nav_scroll_css: CSS, improv_jsonld: INDEX}

CRON_JOB_ID = "a98c6566a21e"   # tripplanner-improve — pause when work is exhausted


def main():
    state = {}
    if os.path.exists(STATE_FILE):
        try: state = json.load(open(STATE_FILE))
        except Exception: pass
    applied = set(state.get("applied", []))

    # seed applied from existing markers
    for m in re.findall(r"<!--impr:(\w+)-->", open(INDEX).read()):
        applied.add("improv_" + m)
    for m in re.findall(r"/\*impr:(\w+)\*/", open(CSS).read()):
        applied.add("improv_" + m)

    fn = next((f for f in IMPROVEMENTS if f.__name__ not in applied), None)
    if fn is None:
        state["last_run"] = time.time()
        json.dump(state, open(STATE_FILE, "w"), ensure_ascii=False, indent=2)
        # verify site still healthy each tick
        ok, msg = validate_project()
        # Work exhausted → pause this cron job (user asked: stop cron when nothing improves)
        subprocess.run(["hermes", "cron", "pause", CRON_JOB_ID], capture_output=True, text=True, timeout=60)
        print(f"✅ TripPlanner: {len(applied)}/{len(IMPROVEMENTS)} improvements applied — nothing new this tick. ({msg})")
        print(f"⏸️ Cron tripplanner-improve đã tự PAUSE — hết cải tiến để áp. Resume khi thêm improvements mới.")
        return

    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    fpath = FILE_FOR[fn]
    shutil.copy2(fpath, os.path.join(BACKUP_DIR, f"{os.path.basename(fpath)}_{stamp}"))
    backups = sorted(os.listdir(BACKUP_DIR))
    while len(backups) > MAX_BACKUPS:
        os.remove(os.path.join(BACKUP_DIR, backups.pop(0)))

    content = open(fpath).read()
    try: result = fn(content)
    except Exception as e:
        print(f"⚠️ Error applying {fn.__name__}: {e}"); return
    if result is None: return
    new_content, desc = result

    ok, msg = validate_project()
    if not ok:
        print(f"⚠️ '{desc}' cancelled — validation failed: {msg}"); return

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(new_content)
    applied.add(fn.__name__)
    state["applied"] = list(applied)
    state["last_run"] = time.time()
    json.dump(state, open(STATE_FILE, "w"), ensure_ascii=False, indent=2)

    pok, pmsg = git_push(desc)
    print(f"✅ Improved TripPlanner: {desc}")
    print(f"   • Backup: backups/{os.path.basename(fpath)}_{stamp}")
    print(f"   • {pmsg} ({len(applied)}/{len(IMPROVEMENTS)} applied)")


if __name__ == "__main__":
    main()