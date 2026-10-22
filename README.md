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
  <YYYY-MM-DD>[_<effort>][-n].html

claude-opus-5-5/
  2026-10-22_medium.html
  2026-10-22_medium-2.html   # second medium-effort giraffe that day
  2026-10-22_high.html
qwen3-27b/
  2026-09-30.html            # no effort setting → no suffix
```

## Naming rules

| Part | Rule | Example |
|------|------|---------|
| `model-slug` | Lowercase kebab-case; dots and spaces → `-`; drop vendor prefixes | `claude-opus-5-5`, `qwen3-27b`, `gpt-4o` |
| `YYYY-MM-DD` | Date the page was **generated** (use the date collected if unknown) | `2026-10-22` |
| `_effort` | Reasoning effort, lowercase, when the model has that setting; omit otherwise | `_low`, `_medium`, `_high`, `_max` |
| `-n` suffix | Only for duplicates with the same model, day, and effort, starting at `-2` | `2026-10-22_medium-2.html` |

Pages should stay single-file: inline JS/CSS, with three.js loaded from a pinned CDN URL.

## Gallery

| Model | Effort | Date | Page |
|-------|--------|------|------|
| claude-opus-5-5 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-opus-5-5/2026-10-22_medium.html) |
| claude-sonnet-5-5 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-sonnet-5-5/2026-10-22_medium.html) |
