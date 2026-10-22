"""Build index.html and the README gallery from the entry folders + entries.json.

Usage:
    python build.py                          # index.html + README gallery
    python build.py --no-readme              # index.html only
"""
import argparse
import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WIKI_GIRAFFE = "https://en.wikipedia.org/wiki/Giraffe"
REPO_URL = "https://github.com/niznik-dev/giraffe-bench"
SITE_URL = "https://niznik-dev.github.io/giraffe-bench/"
PROMPT = "Please create an animation of a giraffe walking through a savannah environment using Three.js"
NAME_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})(?:_(?P<effort>[a-z0-9]+))?(?:-(?P<run>\d+))?$")
VIBES = [  # (key, emoji, name, question, points)
    ("legs", "🦵", "Four legs", "Four legs, attached where legs go?", +1),
    ("walks", "🚶", "Actually walks", "Do the legs carry it forward?", +1),
    ("giraffe", "🦒", "Giraffe-shaped", "Would a child point at it and say 'giraffe'?", +1),
    ("savannah", "🌅", "Real savannah", "Acacias, golden grass, a sky worth looking at?", +1),
    ("nightmare", "😱", "Nightmare fuel", "Will it visit you at 3 a.m.?", -1),
    ("ghost", "👻", "Ghost giraffe", "Clips through the ground, or floats above it?", -1),
    ("wanders", "🚪", "Wanders off", "Leaves the shot while the camera just... watches?", -1),
]
VIBE_KEYS = [v[0] for v in VIBES]
README_START, README_END = "<!-- gallery:start -->", "<!-- gallery:end -->"


def three_version(text):
    if m := re.search(r"three@0\.(\d+)\.\d+", text):
        return f"r{m.group(1)}"
    if m := re.search(r"three\.js/(r\d+)", text):
        return m.group(1)
    return "?"


def load_entries():
    meta = json.loads((ROOT / "entries.json").read_text())
    on_disk = {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.glob("*/*.html")
        if not p.name.endswith(".wrapper.html") and not p.parts[-2].startswith((".", "_"))
    }
    missing, unknown = on_disk - meta["entries"].keys(), meta["entries"].keys() - on_disk
    if missing or unknown:
        raise SystemExit(f"entries.json out of sync.\n  no entry for: {sorted(missing)}\n  no file for: {sorted(unknown)}")

    entries = []
    for path, info in meta["entries"].items():
        file = ROOT / path
        m = NAME_RE.match(file.stem)
        if not m:
            raise SystemExit(f"bad filename: {path}")
        bad = {k: v for k, v in info.get("vibes", {}).items() if k not in VIBE_KEYS or v not in ("yes", "no")}
        if bad:
            raise SystemExit(f"{path}: bad vibes {bad}; keys {VIBE_KEYS}, values yes/no")
        wrapper = file.with_name(file.stem + ".wrapper.html")
        entries.append({
            **info,
            "path": path,
            "slug": file.parent.name,
            "date": m["date"],
            "effort": m["effort"] or "—",
            "run": int(m["run"] or 1),
            "flags": info.get("flags", []),
            "vibes": info.get("vibes", {}),
            "size_kb": round(file.stat().st_size / 1024),
            "three": three_version(file.read_text(errors="ignore")),
            "quant": file.parent.name.rsplit("-", 1)[-1] if info["where"] == "local" else None,
            "wrapper": wrapper.relative_to(ROOT).as_posix() if wrapper.exists() else None,
        })
    entries.sort(key=lambda e: (e["date"], e["where"] != "hosted"), reverse=False)
    pending = meta.get("pending", [])
    hatched = {e["slug"] for e in entries}
    if dupes := [p["slug"] for p in pending if p["slug"] in hatched]:
        raise SystemExit(f"pending entries already have giraffes; remove them from 'pending': {dupes}")
    failed = meta.get("failed", [])
    taken = hatched | {p["slug"] for p in pending}
    if clash := [f["slug"] for f in failed if f["slug"] in taken]:
        raise SystemExit(f"failed entries also appear in the herd or as eggs: {clash}")
    return meta["flags"], entries, pending, failed


# ---------- README ----------

def gp(e):
    """Giraffe Points: bonuses earned minus penalties incurred; None until every check is judged."""
    if any(k not in e["vibes"] for k in VIBE_KEYS):
        return None
    return sum(points for key, *_, points in VIBES if e["vibes"][key] == "yes")


def fmt_gp(e):
    return "?" if (score := gp(e)) is None else f"{score:+d}"


def readme_gallery(flags, entries, pending, failed):
    lines = ["| Model | Effort | Date | Page | GP | Vibe check | ⚑ |", "|-------|--------|------|------|----|------------|---|"]
    for e in entries:
        name = Path(e["path"]).name
        bonus = "".join(emoji for key, emoji, *_, pts in VIBES if pts > 0 and e["vibes"].get(key) == "yes")
        penalty = "".join(emoji for key, emoji, *_, pts in VIBES if pts < 0 and e["vibes"].get(key) == "yes")
        unjudged = sum(k not in e["vibes"] for k in VIBE_KEYS)
        vibes = " ".join(filter(None, [bonus and f"+{bonus}", penalty and f"−{penalty}", unjudged and f"❔×{unjudged}"]))
        lines.append(f"| {e['slug']} | {e['effort']} | {e['date']} | [{name}]({e['path']}) | **{fmt_gp(e)}** | {vibes} | {' '.join(e['flags'])} |")
    lines += ["", "**Giraffe Points (GP)** = bonuses − penalties. "
              "Bonuses: " + " · ".join(f"{emoji} {name.lower()}" for _, emoji, name, _, pts in VIBES if pts > 0) + ". "
              "Penalties: " + " · ".join(f"{emoji} {name.lower()}" for _, emoji, name, _, pts in VIBES if pts < 0) + "."]
    for emoji, flag in flags.items():
        flagged = [e for e in entries if emoji in e["flags"]]
        if not flagged:
            continue
        lines += ["", f"{emoji} **{flag['title']}.** {flag['text']}"]
        tagged = [e for e in flagged if e.get("tag")]
        if tagged:
            lines += ["", "| Model | Ollama tag | Likely thinking level |", "|-------|------------|-----------------------|"]
            lines += [f"| {e['slug']} | `{e['tag']}` | `{e.get('thinking_guess', '?')}` (unverified) |" for e in tagged]
        wrapped = [e for e in flagged if e["wrapper"]]
        if wrapped:
            lines += ["Originals: " + " · ".join(f"[{e['slug']} {e['effort']}]({e['wrapper']})" for e in wrapped) + "."]
    for f in failed:
        lines += ["", f"🪦 **Graveyard: {f['label']}** (`{f['tag']}`). {f['epitaph']}"]
    if pending:
        lines += ["", "🥚 **Incubating:** " + " · ".join(f"{p['label']} (`{p['tag']}`)" for p in pending) + "."]
    return "\n".join(lines)


def write_readme(flags, entries, pending, failed):
    readme = ROOT / "README.md"
    text = readme.read_text()
    if README_START not in text:
        raise SystemExit(f"README.md needs {README_START} / {README_END} markers around the gallery")
    head, rest = text.split(README_START, 1)
    _, tail = rest.split(README_END, 1)
    readme.write_text(f"{head}{README_START}\n{readme_gallery(flags, entries, pending, failed)}\n{README_END}{tail}")


# ---------- index.html ----------

def esc(s):
    return html.escape(str(s), quote=True)


def lessons(entries):
    by_three = defaultdict(list)
    for e in entries:
        by_three[e["three"]].append(e["label"])
    three_items = "".join(
        f"<li><b>three.js {esc(v)}</b> × {len(labels)} — {esc(', '.join(sorted(set(labels))))}</li>"
        for v, labels in sorted(by_three.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    )
    small = min(entries, key=lambda e: e["size_kb"])
    big = max(entries, key=lambda e: e["size_kb"])
    detours = sum("😵‍💫" in e["flags"] for e in entries)
    fixes = sum("🔧" in e["flags"] for e in entries)
    judged = [e for e in entries if e["vibes"]]
    if judged:
        vibe_items = "".join(
            f"<li>{emoji} <b>{esc(name)}</b>: {sum(e['vibes'].get(key) == 'yes' for e in judged)} of {len(judged)}</li>"
            for key, emoji, name, _, _ in VIBES
        )
        scored = [e for e in entries if gp(e) is not None]
        top = ""
        if scored:
            best = max(gp(e) for e in scored)
            leaders = sorted({e["label"] for e in scored if gp(e) == best})
            top = f"<p>🏆 Top score <b>{best:+d} GP</b>: {esc(', '.join(leaders))}.</p>"
        vibe_body = f"{top}<ul>{vibe_items}</ul><p class=\"aside\">Judged by one human with taste.</p>"
    else:
        vibe_body = "<p>The jury is still out. 🧑‍⚖️</p>"
    local = sum(e["where"] == "local" for e in entries)
    return f"""
    <div class="lessons">
      <div class="lesson"><span class="big">📦</span><h3>Which three.js?</h3><ul>{three_items}</ul>
        <p class="aside">r128 is from 2021: the version all over the training data.</p></div>
      <div class="lesson"><span class="big">📏</span><h3>Giraffe mass</h3>
        <p>Smallest: <b>{esc(small['label'])}</b> at {small['size_kb']} KB.<br>
        Biggest: <b>{esc(big['label'])}</b> at {big['size_kb']} KB.</p>
        <p class="aside">Bytes are not legs. Size measures ambition, not gait.</p></div>
      <div class="lesson"><span class="big">🧭</span><h3>Getting a file at all</h3>
        <p><b>{detours + fixes}</b> of {len(entries)} giraffes needed a follow-up prompt: {detours} 😵‍💫 to get a file at all,
        {fixes} 🔧 to fix a broken one.
        <b>{local}</b> ran on a laptop.</p>
        <p class="aside">The app around a model shapes the result as much as the model does.</p></div>
      <div class="lesson"><span class="big">🔍</span><h3>Vibe check</h3>{vibe_body}</div>
    </div>"""


def card(e, flags, order):
    page = esc(e["path"])
    title = esc(e["label"])
    flag_html = "".join(
        f'<span class="flag" title="{esc(flags[f]["title"])}: {esc(flags[f]["text"])}">{f}</span>' for f in e["flags"]
    )
    chips = [
        ("☁️ hosted" if e["where"] == "hosted" else "💻 local", ""),
        (f"🧠 {e['effort']}", "effort / thinking setting"),
        (f"📦 three {e['three']}", "three.js version"),
        (f"📏 {e['size_kb']} KB", "file size"),
    ]
    if e["quant"]:
        chips.insert(1, (f"🗜️ {e['quant']}", "quantization"))
    if e["run"] > 1:
        chips.append((f"🔁 run {e['run']}", ""))
    chip_html = "".join(f'<span class="chip" title="{esc(t)}">{esc(c)}</span>' for c, t in chips)

    walk = "“walk”" if e["vibes"].get("walks") == "no" else "walk"
    stage = (f'<div class="stage" data-src="{page}"><button class="start" type="button">'
             f'<span class="emoji">🦒</span>▶ Watch it {walk}</button></div>')

    def vibe_row(sign, label):
        spans = []
        for key, emoji, name, question, pts in VIBES:
            if (pts > 0) != (sign > 0):
                continue
            verdict = e["vibes"].get(key)
            state = {"yes": "on", "no": "off"}.get(verdict, "unknown")
            mark = {"yes": f"{pts:+d}", "no": "0"}.get(verdict, "not judged yet")
            spans.append(f'<span class="vibe {state}" title="{esc(name)}: {esc(question)} ({mark})">{emoji}</span>')
        return f'<div class="vibes {label}"><span class="rowlabel">{"🌟 Bonus" if sign > 0 else "💀 Penalty"}</span>{"".join(spans)}</div>'

    score = gp(e)
    gp_class = "unknown" if score is None else "pos" if score > 0 else "neg" if score < 0 else "zero"
    vibes = vibe_row(+1, "bonus") + vibe_row(-1, "penalty")

    extra = ""
    if e.get("tag"):
        extra += f'<p class="tag">Ollama tag <code>{esc(e["tag"])}</code>, likely thinking <code>{esc(e.get("thinking_guess", "?"))}</code></p>'
    links = [f'<a href="{page}" target="_blank" rel="noopener">↗ full screen</a>',
             f'<a href="{REPO_URL}/blob/main/{page}" target="_blank" rel="noopener">📜 source</a>']
    if e["wrapper"]:
        links.append(f'<a href="{esc(e["wrapper"])}" target="_blank" rel="noopener">🎁 as delivered</a>')
    return f"""
      <article class="card" data-order="{order}" data-gp="{'' if score is None else score}" data-size="{e['size_kb']}" data-name="{title}">
        {stage}
        <div class="body">
          <h3>{title} <span class="flags">{flag_html}</span></h3>
          <p class="meta">{esc(e['date'])} <span class="gp {gp_class}" title="Giraffe Points: bonuses minus penalties">{fmt_gp(e)} GP</span></p>
          {vibes}
          <div class="chips">{chip_html}</div>
          {extra}
          <nav class="links">{' '.join(links)}</nav>
        </div>
      </article>"""


THEME_SCRIPT = """
// The sun is a day/night switch; it starts from the visitor's system theme.
(() => {
  const root = document.documentElement, dark = matchMedia('(prefers-color-scheme: dark)');
  const isNight = () => root.dataset.theme ? root.dataset.theme === 'dark' : dark.matches;
  const sun = document.querySelector('.sun');
  const label = () => sun.title = isNight() ? 'Bring back the sun' : 'Send the sun to bed';
  sun.addEventListener('click', () => {
    root.dataset.theme = isNight() ? 'light' : 'dark';
    try { localStorage.setItem('giraffe-theme', root.dataset.theme); } catch (e) {}
    label();
  });
  dark.addEventListener('change', label);
  label();
})();
"""


WALKER_SCRIPT = """
// Walk the hero giraffe along the ground curve, tilting with the slope.
(() => {
  const walker = document.querySelector('.walker'), ground = document.getElementById('ground');
  const layer = walker.parentElement;  // pinned to the same box as the ground SVG
  const VIEW_W = 1200, LAP_MS = 38000, SINK = 6;
  const groundY = new Float32Array(VIEW_W + 1);  // ground height at each viewBox x
  for (let len = 0, total = ground.getTotalLength(); len <= total; len += 0.5) {
    const pt = ground.getPointAtLength(len);
    if (pt.x > VIEW_W || pt.y > 125) break;  // past the top edge, into the V/H closing segments
    groundY[Math.round(pt.x)] = pt.y;
  }
  const yAt = x => groundY[Math.max(0, Math.min(VIEW_W, Math.round(x)))];
  let box;
  const measure = () => {
    const w = layer.clientWidth;
    box = {top: 0, scaleX: w / VIEW_W, scaleY: layer.clientHeight / 130, width: w, size: walker.offsetHeight};
  };
  const place = px => {
    const vx = px / box.scaleX, y = box.top + yAt(vx) * box.scaleY;
    const slope = (yAt(vx + 8) - yAt(vx - 8)) * box.scaleY / (16 * box.scaleX);
    const angle = Math.atan(slope) * 180 / Math.PI;
    walker.style.transform = `translate(${px - box.size / 2}px, ${y - box.size + SINK}px) rotate(${angle}deg) scaleX(-1)`;
  };
  measure();
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const still = () => { measure(); place(box.width * 0.12); };
    still(); addEventListener('resize', still); document.fonts?.ready.then(still);
    return;
  }
  const tick = () => {
    measure();
    const span = box.width + 2 * box.size;
    place((performance.now() % LAP_MS) / LAP_MS * span - box.size);
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})();
"""


SORT_SCRIPT = """
// Re-order cards in place; eggs stay last, ties fall back to the built (most-cursed) order.
(() => {
  const grid = document.querySelector('.grid'), buttons = document.querySelectorAll('.sorter button');
  const num = (el, k, missing) => el.dataset[k] ? Number(el.dataset[k]) : missing;
  const keys = {
    cursed: () => 0,
    best: (a, b) => num(b, 'gp', -Infinity) - num(a, 'gp', -Infinity),
    size: (a, b) => num(b, 'size', 0) - num(a, 'size', 0),
    name: (a, b) => a.dataset.name.localeCompare(b.dataset.name),
  };
  const apply = mode => {
    const cards = [...grid.children];
    const eggs = cards.filter(c => 'egg' in c.dataset), herd = cards.filter(c => !('egg' in c.dataset));
    herd.sort((a, b) => keys[mode](a, b) || num(a, 'order', 0) - num(b, 'order', 0));
    grid.append(...herd, ...eggs);
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.sort === mode)));
  };
  buttons.forEach(b => b.addEventListener('click', () => {
    apply(b.dataset.sort);
    try { localStorage.setItem('giraffe-sort', b.dataset.sort); } catch (e) {}
  }));
  try { const saved = localStorage.getItem('giraffe-sort'); if (saved in keys) apply(saved); } catch (e) {}
})();
"""


SCRIPT = """
document.querySelectorAll('.stage[data-src]').forEach(stage => {
  const idle = stage.innerHTML;
  stage.addEventListener('click', ev => {
    if (!ev.target.closest('.start')) return;
    stage.innerHTML = '';
    const f = document.createElement('iframe');
    f.src = stage.dataset.src; f.title = 'giraffe'; f.setAttribute('sandbox', 'allow-scripts');
    const stop = document.createElement('button');
    stop.className = 'stop'; stop.type = 'button'; stop.textContent = '■ stop';
    stop.addEventListener('click', () => { stage.innerHTML = idle; });
    stage.append(f, stop);
  });
});"""


NIGHT_VARS = """--bg: #15121a; --ink: #f1e9dc; --muted: #b3a690; --card: #211c26; --line: #3a3241;
    --accent: #f0a04b; --accent-ink: #1b1510; --chip: #2f2833; --sky1: #0b1030; --sky2: #1f2150; --sky3: #4b3a6e;
    --ground: #3a2c1f; --tree: #0a0808;"""


def night_css(sel):
    return f"""{sel} {{ {NIGHT_VARS} }}
{sel} .sun {{ background:
    radial-gradient(circle at 58% 38%, rgba(0,0,0,.10) 0 7%, transparent 8%),
    radial-gradient(circle at 42% 62%, rgba(0,0,0,.08) 0 5%, transparent 6%),
    radial-gradient(circle at 36% 34%, #fffef6, #e9e5d6 50%, #cbc5b0 66%, transparent 68%);
  filter: drop-shadow(0 0 18px rgba(255,250,220,.45)); opacity: 1; }}
{sel} .stars {{ opacity: 1; }}"""


def stars_shadow(n=70, seed=7):
    import random
    rng = random.Random(seed)
    return ", ".join(
        f"{rng.randint(0, 1600)}px {rng.randint(0, 230)}px 0 {rng.choice(['0', '0', '1px'])} rgba(255,255,240,{rng.uniform(.4, .95):.2f})"
        for _ in range(n)
    )


def egg_card(p):
    return f"""
      <article class="card egg" data-egg>
        <div class="stage nest"><span class="emoji">🥚</span><span>incubating…</span></div>
        <div class="body">
          <h3>{esc(p['label'])}</h3>
          <div class="chips"><span class="chip">💻 local</span><span class="chip">🏷️ {esc(p['tag'])}</span></div>
          <p class="tag">Not run yet. Check back for a giraffe (or a horror).</p>
        </div>
      </article>"""


def grave_card(f):
    return f"""
      <article class="card grave">
        <div class="stage tomb"><span class="emoji">🪦</span><span>no giraffe survived</span></div>
        <div class="body">
          <h3>{esc(f['label'])}</h3>
          <div class="chips"><span class="chip">💻 local</span><span class="chip">🏷️ {esc(f['tag'])}</span></div>
          <p class="epitaph">{esc(f['epitaph'])}</p>
        </div>
      </article>"""


def render_index(flags, entries, pending, failed):
    graveyard = ""
    if failed:
        graveyard = ('<h2 class="section graveyard-head">🪦 Giraffe graveyard</h2>\n'
                     '  <p class="aside">Models that never produced a working giraffe. Gone, but not forgotten.</p>\n'
                     f'  <div class="grid">{"".join(grave_card(f) for f in failed)}\n  </div>')
    # Server-side order is "most cursed": lowest GP first, unscored last, ties by name.
    cursed = sorted(entries, key=lambda e: (gp(e) is None, gp(e) or 0, e["label"], e["effort"]))
    cards = "".join(card(e, flags, i) for i, e in enumerate(cursed))
    models = len({e["slug"] for e in entries})
    legend = "".join(
        f'<li><span class="flag">{f}</span> <b>{esc(v["title"])}.</b> {esc(v["text"])}</li>' for f, v in flags.items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>giraffe-bench 🦒</title>
<meta name="description" content="LLM-generated three.js giraffes walking through a savannah. Not a serious benchmark.">
<meta property="og:title" content="giraffe-bench 🦒">
<meta property="og:description" content="{len(entries)} LLM-generated three.js giraffes, walking with varying success.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🦒</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;700&family=Nunito:wght@400;700&display=swap" rel="stylesheet">
<script>try {{ const t = localStorage.getItem('giraffe-theme'); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}</script>
<style>
:root {{
  --bg: #fdf6e9; --ink: #2b2118; --muted: #7a6650; --card: #fffdf8; --line: #ead9bd;
  --accent: #d9822b; --accent-ink: #fff; --chip: #f6ead3; --sky1: #ffcf7a; --sky2: #f08a4b; --sky3: #c2475e;
  --ground: #b9893f; --tree: #3b2a1d;
}}
@media (prefers-color-scheme: dark) {{
{night_css(':root:not([data-theme="light"])')}
}}
{night_css(':root[data-theme="dark"]')}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 Nunito, system-ui, sans-serif; }}
h1, h2, h3 {{ font-family: Fredoka, Nunito, sans-serif; line-height: 1.15; }}
a {{ color: var(--accent); }}
.wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 16px; }}
header.hero {{ position: relative; overflow: hidden; color: #fff;
  background: linear-gradient(180deg, var(--sky1), var(--sky2) 55%, var(--sky3)); padding: 56px 0 120px; }}
.hero h1 {{ font-size: clamp(2.4rem, 7vw, 4.2rem); margin: 0; text-shadow: 0 3px 0 rgba(0,0,0,.18); }}
.hero .tagline {{ font-size: 1.2rem; margin: 8px 0 20px; max-width: 40ch; }}
.hero blockquote {{ margin: 0; padding: 14px 18px; background: rgba(0,0,0,.22); border-radius: 14px;
  max-width: 62ch; font-size: 1.05rem; backdrop-filter: blur(2px); }}
.hero blockquote small {{ display: block; opacity: .8; margin-top: 4px; }}
.hero svg {{ position: absolute; left: 0; right: 0; bottom: -1px; width: 100%; height: 130px; }}
.sun {{ position: absolute; right: 8%; top: 40px; width: 110px; height: 110px; border-radius: 50%; border: 0; padding: 0;
  background: radial-gradient(circle, #fff3c4, #ffd36e 60%, transparent 70%); opacity: .9; cursor: pointer;
  transition: transform .3s; z-index: 1; }}
.sun:hover {{ transform: scale(1.08) rotate(-8deg); }}
.sun:focus-visible {{ outline: 3px solid #fff; outline-offset: 4px; }}
.stars {{ position: absolute; inset: 0; pointer-events: none; opacity: 0; transition: opacity .6s; }}
.stars::before {{ content: ""; position: absolute; left: 0; top: 0; width: 1px; height: 1px; border-radius: 50%;
  box-shadow: {stars_shadow()}; }}
a.wiki {{ text-decoration: none; color: inherit; cursor: pointer; display: inline-block; transition: transform .15s; }}
h1 a.wiki:hover, .stats a.wiki:hover {{ transform: rotate(-12deg) scale(1.15); }}
.ground-layer {{ position: absolute; left: 0; right: 0; bottom: -1px; height: 130px; z-index: 1; pointer-events: none; }}
.walker {{ position: absolute; left: 0; top: 0; pointer-events: auto; font-size: 44px; line-height: 1;
  transform-origin: 50% 100%; will-change: transform; }}
@media (max-width: 600px) {{ .sun {{ width: 64px; height: 64px; top: 12px; right: 12px; }} }}
.disclaimer {{ margin: -48px auto 28px; position: relative; background: var(--card); border: 2px dashed var(--accent);
  border-radius: 18px; padding: 18px 22px; }}
.disclaimer h2 {{ margin: 0 0 6px; font-size: 1.35rem; }}
.disclaimer p {{ margin: 6px 0; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 10px; margin: 12px 0 0; padding: 0; list-style: none; }}
.stats li {{ background: var(--chip); border-radius: 999px; padding: 4px 12px; font-weight: 700; }}
.lessons {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 0 0 36px; }}
.lesson {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px; }}
.lesson h3 {{ margin: 4px 0 8px; }}
.lesson ul {{ margin: 0; padding-left: 18px; }}
.lesson .big {{ font-size: 1.8rem; }}
.aside {{ color: var(--muted); font-size: .92rem; font-style: italic; }}
h2.section {{ font-size: 1.8rem; margin: 8px 0 14px; }}
.herd-head {{ display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 8px 16px; }}
.sorter {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-bottom: 14px; }}
.sort-label {{ color: var(--muted); font-weight: 700; font-size: .9rem; }}
.sorter button {{ font: 700 .88rem Nunito, sans-serif; color: var(--ink); background: var(--chip); border: 2px solid transparent;
  border-radius: 999px; padding: 4px 12px; cursor: pointer; }}
.sorter button:hover {{ border-color: var(--line); }}
.sorter button[aria-pressed="true"] {{ background: var(--accent); color: var(--accent-ink); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
.card {{ background: var(--card); border: 1px solid var(--line); border-radius: 18px; overflow: hidden;
  display: flex; flex-direction: column; transition: transform .15s, box-shadow .15s; }}
.card:hover {{ transform: translateY(-3px) rotate(-.3deg); box-shadow: 0 10px 24px rgba(0,0,0,.12); }}
.stage {{ position: relative; aspect-ratio: 16 / 10; background: linear-gradient(180deg, var(--sky1), var(--sky2));
  display: grid; place-items: center; overflow: hidden; color: #fff; text-decoration: none; }}
.stage iframe {{ position: absolute; inset: 0; width: 100%; height: 100%; border: 0; background: #000; }}
.start {{ font: 700 1.05rem Fredoka, sans-serif; color: var(--accent-ink); background: var(--accent); border: 0;
  border-radius: 999px; padding: 10px 18px; cursor: pointer; display: flex; align-items: center; gap: 8px;
  box-shadow: 0 4px 0 rgba(0,0,0,.2); }}
.start:hover .emoji {{ display: inline-block; animation: bob .5s ease-in-out infinite alternate; }}
@keyframes bob {{ to {{ transform: translateY(-4px) rotate(6deg); }} }}
.start .emoji {{ font-size: 1.4rem; }}
.stop {{ position: absolute; right: 8px; top: 8px; z-index: 1; font: 700 .8rem Nunito, sans-serif; border: 0;
  border-radius: 999px; padding: 4px 10px; background: rgba(0,0,0,.6); color: #fff; cursor: pointer; }}
.body {{ padding: 14px 16px 16px; display: flex; flex-direction: column; gap: 8px; flex: 1; }}
.body h3 {{ margin: 0; font-size: 1.2rem; display: flex; justify-content: space-between; gap: 8px; }}
.meta {{ margin: -6px 0 0; color: var(--muted); font-size: .9rem; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.chip {{ background: var(--chip); border-radius: 999px; padding: 2px 10px; font-size: .85rem; white-space: nowrap; }}
.flag {{ cursor: help; }}
.meta {{ display: flex; justify-content: space-between; align-items: center; }}
.gp {{ font: 700 1.05rem Fredoka, sans-serif; padding: 2px 12px; border-radius: 999px; background: var(--chip); color: var(--ink); }}
.gp.pos {{ background: #2f9e55; color: #fff; }} .gp.neg {{ background: #c2475e; color: #fff; }}
.graveyard-head {{ margin-top: 40px; }}
.grave {{ filter: grayscale(.85); opacity: .8; }}
.grave:hover {{ transform: none; box-shadow: none; filter: grayscale(.4); }}
.tomb {{ display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 4px; font: 600 1rem Fredoka, sans-serif;
  background: linear-gradient(180deg, #3d3a4a, #22202b); color: #ddd; }}
.tomb .emoji {{ font-size: 2.8rem; }}
.epitaph {{ margin: 0; font-style: italic; color: var(--muted); font-size: .92rem; }}
.egg {{ opacity: .75; border-style: dashed; }}
.egg:hover {{ transform: none; box-shadow: none; }}
.nest {{ display: flex; align-items: center; justify-content: center; flex-direction: column; gap: 4px; font: 600 1rem Fredoka, sans-serif; }}
.nest .emoji {{ font-size: 2.8rem; display: inline-block; animation: wobble 2.4s ease-in-out infinite; }}
@keyframes wobble {{ 0%, 70%, 100% {{ transform: rotate(0); }} 76% {{ transform: rotate(-12deg); }} 84% {{ transform: rotate(10deg); }} 92% {{ transform: rotate(-5deg); }} }}
@media (prefers-reduced-motion: reduce) {{ .nest .emoji {{ animation: none; }} }}
.vibes {{ display: flex; gap: 6px; align-items: center; }}
.rowlabel {{ flex: 0 0 7.6em; box-sizing: border-box; font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .04em;
  color: var(--muted); border-right: 2px solid var(--line); padding-right: 8px; margin-right: 2px; white-space: nowrap; }}
.vibe {{ cursor: help; border-radius: 10px; padding: 1px 6px; font-size: 1.15rem; border: 2px solid transparent; }}
.vibe.off {{ opacity: .22; filter: grayscale(1); }}
.vibe.unknown {{ opacity: .45; border: 2px dashed var(--line); }}
.bonus .vibe.on {{ background: rgba(47,158,85,.16); border-color: #2f9e55; }}
.penalty .vibe.on {{ background: rgba(194,71,94,.16); border-color: #c2475e; }}
.tag {{ margin: 0; font-size: .85rem; color: var(--muted); }}
code {{ font-size: .85em; background: var(--chip); padding: 1px 5px; border-radius: 6px; }}
.links {{ margin-top: auto; display: flex; flex-wrap: wrap; gap: 4px 14px; font-weight: 700; font-size: .92rem; }}
.links a {{ text-decoration: none; }} .links a:hover {{ text-decoration: underline; }}
.legend {{ list-style: none; padding: 0; margin: 28px 0; display: grid; gap: 8px; color: var(--muted); }}
footer {{ border-top: 1px solid var(--line); margin-top: 40px; padding: 24px 0 40px; color: var(--muted); font-size: .95rem; }}
</style>
</head>
<body>
<header class="hero">
  <div class="stars" aria-hidden="true"></div>
  <button class="sun" type="button" aria-label="Toggle day and night" title="Toggle day / night"></button>
  <div class="wrap">
    <h1>giraffe-bench <a class="wiki" href="{WIKI_GIRAFFE}" target="_blank" rel="noopener" title="Meet a real giraffe (Wikipedia)">🦒</a></h1>
    <p class="tagline">One prompt. Many models. Varying numbers of legs.</p>
    <blockquote>“{esc(PROMPT)}”<small>The exact prompt every model received.</small></blockquote>
  </div>
  <div class="ground-layer"><a class="walker wiki" href="{WIKI_GIRAFFE}" target="_blank" rel="noopener" title="Meet a real giraffe (Wikipedia)">🦒</a></div>
  <svg viewBox="0 0 1200 130" preserveAspectRatio="none" aria-hidden="true">
    <path id="ground" d="M0 70 Q 150 50 300 64 Q 460 78 620 62 Q 760 46 900 64 Q 1050 78 1200 58 V130 H0Z" fill="var(--ground)"/>
    <path d="M0 100 Q 200 88 420 102 T 820 96 T 1200 100 V130 H0Z" fill="var(--bg)"/>
    <g fill="var(--tree)">
      <rect x="168" y="22" width="6" height="38"/><ellipse cx="171" cy="20" rx="52" ry="11"/>
      <rect x="958" y="22" width="7" height="48"/><ellipse cx="961" cy="20" rx="64" ry="13"/>
    </g>
  </svg>
</header>

<main class="wrap">
  <section class="disclaimer">
    <h2>⚠️ This is a Very Serious Benchmark™ (it is not)</h2>
    <p>One giraffe per model, one prompt, zero rubric. Scoring is by vibes and leg count. Hosted models ran on their
    vendors' servers; local ones ran on a laptop. Treat it as a field guide, not a leaderboard.</p>
    <p>Still, a herd shows patterns a single giraffe can't. Here's what we've spotted so far 👇</p>
    <ul class="stats">
      <li><a class="wiki" href="{WIKI_GIRAFFE}" target="_blank" rel="noopener" title="Meet a real giraffe (Wikipedia)">🦒</a> {len(entries)} giraffes</li><li>🧬 {models} models</li>
      <li>☁️ {sum(e['where'] == 'hosted' for e in entries)} hosted</li>
      <li>💻 {sum(e['where'] == 'local' for e in entries)} local</li>
      {f"<li>🪦 {len(failed)} lost</li>" if failed else ""}
    </ul>
  </section>
  {lessons(entries)}

  <div class="herd-head">
    <h2 class="section">The herd</h2>
    <div class="sorter" role="group" aria-label="Sort the herd">
      <span class="sort-label">Sort:</span>
      <button type="button" data-sort="cursed" aria-pressed="true">😱 Most cursed</button>
      <button type="button" data-sort="best" aria-pressed="false">🏆 Best</button>
      <button type="button" data-sort="size" aria-pressed="false">📏 Size</button>
      <button type="button" data-sort="name" aria-pressed="false">🔤 Name</button>
    </div>
  </div>
  <div class="grid">{cards}{"".join(egg_card(p) for p in pending)}
  </div>
  {graveyard}

  <ul class="legend">{legend}</ul>
</main>

<footer>
  <div class="wrap">
    <p>Started as a live demo for the October 2026 meeting of Princeton Research Computing's
    <a href="https://researchcomputing.princeton.edu/learn/user-groups/llm-collective">LLM Collective</a>.
    Thanks to <a href="https://github.com/pilambdaepsilon">Pedro Espino</a> for suggesting the giraffe, and to
    <a href="https://www.reddit.com/r/ClaudeAI/comments/1wpq8by/testing_claude_for_3d_creation_max_took_a_whole/">this r/ClaudeAI post</a>
    for the original idea.</p>
    <p>Pages are model output, shown as delivered and sandboxed. 🐙 <a href="{REPO_URL}">Source, naming rules &amp; how to add a giraffe</a></p>
  </div>
</footer>
<script>{THEME_SCRIPT}{WALKER_SCRIPT}{SORT_SCRIPT}{SCRIPT}
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="index.html")
    ap.add_argument("--no-readme", action="store_true")
    args = ap.parse_args()

    flags, entries, pending, failed = load_entries()
    (ROOT / args.out).write_text(render_index(flags, entries, pending, failed))
    print(f"wrote {args.out} ({len(entries)} entries, {len(pending)} incubating, {len(failed)} lost)")
    if not args.no_readme:
        write_readme(flags, entries, pending, failed)
        print("updated README.md gallery")


if __name__ == "__main__":
    main()
