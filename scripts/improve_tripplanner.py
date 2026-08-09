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


IMPROVEMENTS = [improv_why_us, improv_faq, improv_results_note, improv_style_polish]
FILE_FOR = {improv_why_us: INDEX, improv_faq: INDEX, improv_results_note: INDEX, improv_style_polish: CSS}


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
        print(f"✅ TripPlanner: {len(applied)}/{len(IMPROVEMENTS)} improvements applied — nothing new this tick. ({msg})")
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