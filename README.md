# giraffe-bench 🦒

A herd of single-page three.js sites, each one an LLM's attempt at **a giraffe galloping**.
Every file is self-contained: open it in a browser and watch the legs (hopefully) move.

## Layout

```
<model-slug>/
  <YYYY-MM-DD>.html
  <YYYY-MM-DD>-2.html   # second giraffe from the same model on the same day
```

## Naming rules

| Part | Rule | Example |
|------|------|---------|
| `model-slug` | Lowercase kebab-case; dots and spaces → `-`; drop vendor prefixes | `claude-opus-5-5`, `qwen3-27b`, `gpt-4o` |
| `YYYY-MM-DD` | Date the page was **generated** (use the date collected if unknown) | `2026-10-22` |
| `-n` suffix | Only for same-model, same-day duplicates, starting at `-2` | `2026-10-22-2.html` |

Pages should stay single-file: inline JS/CSS, with three.js loaded from a pinned CDN URL.

## Gallery

| Model | Date | Page |
|-------|------|------|
| _empty paddock — giraffes incoming_ | | |
