# giraffe-bench 🦒

A herd of single-page three.js sites, each one an LLM's answer to the same prompt.
Every file is self-contained: open it in a browser and watch the legs (hopefully) move.

## Prompt

> Please create an animation of a giraffe walking through a savannah environment using Three.js

Every entry uses this exact prompt. If the wording ever changes, record the new version here
and note which entries used it.

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
