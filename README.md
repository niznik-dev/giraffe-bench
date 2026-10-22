# giraffe-bench 🦒

A herd of single-page three.js sites, each one an LLM's answer to the same prompt:

> Please create an animation of a giraffe walking through a savannah environment using Three.js

**🌍 Live gallery: <https://niznik-dev.github.io/giraffe-bench/>.** Click any page below to watch the
giraffe (hopefully) walk.

Started as a live demo for the October 2026 meeting of Princeton Research Computing's
[LLM Collective](https://researchcomputing.princeton.edu/learn/user-groups/llm-collective).
Thanks to [Pedro Espino](https://github.com/pilambdaepsilon) for suggesting the giraffe, and to
[this r/ClaudeAI post](https://www.reddit.com/r/ClaudeAI/comments/1wpq8by/testing_claude_for_3d_creation_max_took_a_whole/)
for the original idea of testing models on 3D creation.

## Gallery

| Model | Effort | Date | Page | ⚑ |
|-------|--------|------|------|---|
| claude-opus-5-5 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-opus-5-5/2026-10-22_medium.html) | |
| claude-sonnet-5-5 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-sonnet-5-5/2026-10-22_medium.html) | |
| claude-haiku-5-5 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-haiku-5-5/2026-10-22_medium.html) | |
| chatgpt-sol-6-1 | xhigh | 2026-10-22 | [2026-10-22_xhigh.html](chatgpt-sol-6-1/2026-10-22_xhigh.html) | 😵‍💫 |
| chatgpt-sol-6-1 | medium | 2026-10-22 | [2026-10-22_medium.html](chatgpt-sol-6-1/2026-10-22_medium.html) | 😵‍💫 |
| nemotron-3-5-lightning-30b-nvfp4 | default | 2026-10-22 | [2026-10-22_default.html](nemotron-3-5-lightning-30b-nvfp4/2026-10-22_default.html) | 💻 |
| muse-glimmer-30b-nvfp4 | default | 2026-10-22 | [2026-10-22_default.html](muse-glimmer-30b-nvfp4/2026-10-22_default.html) | 💻 |
| gemma4-12b-q4km | default | 2026-10-22 | [2026-10-22_default.html](gemma4-12b-q4km/2026-10-22_default.html) | 💻 |

💻 **Local run.** MacBook Pro (Apple M2 Pro, 32 GB) through Cherry Studio → Ollama 0.40.4. Effort is
Cherry's thinking setting; the level Ollama actually ran is a best guess from each model's default.

| Model | Ollama tag | Likely thinking level |
|-------|------------|-----------------------|
| nemotron-3-5-lightning-30b-nvfp4 | `nemotron-3.5-lightning:30b-mlx` | `true` (unverified) |
| muse-glimmer-30b-nvfp4 | `muse-glimmer:30b-mlx` | `high` (unverified) |
| gemma4-12b-q4km | `gemma4:12b` | `true` (unverified) |

😵‍💫 **ChatGPT detour.** The first reply wasn't obviously an HTML file. Asked *"Is this an HTML file I
can download?"* and received a viewer-wrapped HTML file; the giraffe page was recovered from inside it.
Originals: [xhigh](chatgpt-sol-6-1/2026-10-22_xhigh.wrapper.html) ·
[medium](chatgpt-sol-6-1/2026-10-22_medium.wrapper.html).

## Contributing

Every entry uses the exact prompt above. If the wording ever changes, record the new version here
and note which entries used it. Pages should stay single-file: inline JS/CSS, with three.js loaded
from a pinned CDN URL. Anything that differs from a clean one-shot run (follow-up prompts,
extraction, a different machine or runtime) gets a ⚑ emoji in the gallery and a legend entry below it.

<details markdown="1">
<summary><b>Layout</b></summary>

```
<model-slug>/
  <YYYY-MM-DD>[_<effort>][-n].html

claude-opus-5-5/
  2026-10-22_medium.html
  2026-10-22_medium-2.html   # second medium-effort giraffe that day
  2026-10-22_high.html
qwen3-27b-q4km/
  2026-09-30.html            # local model: quant in folder, no effort suffix
```

</details>

<details markdown="1">
<summary><b>Naming rules</b></summary>

| Part | Rule | Example |
|------|------|---------|
| `model-slug` | Lowercase kebab-case; dots and spaces → `-`; drop vendor prefixes, but keep a product name when the model name is obscure without it | `claude-opus-5-5`, `qwen3-27b`, `chatgpt-sol-6-1` |
| `-quant` (local models) | Appended to the model slug: lowercase, punctuation dropped. Hosted models omit it. Runtime (Ollama, llama.cpp, transformers…) goes in the 💻 legend | `qwen3-27b-q4km/`, `qwen3-27b-bf16/` |
| `YYYY-MM-DD` | Date the page was **generated** (use the date collected if unknown) | `2026-10-22` |
| `_effort` | Reasoning effort, lowercase, **no hyphens** (they'd clash with `-n`); omit if the model has no such setting. Local runs use Cherry Studio's thinking setting as chosen; the 💻 legend gives a best guess at the level Ollama ran | `_low`, `_medium`, `_high`, `_xhigh`, `_max`; local: `_default`, `_off`, `_auto` |
| `-n` suffix | Only for duplicates with the same model, day, and effort, starting at `-2` | `2026-10-22_medium-2.html` |
| `.wrapper` | The original, unedited file, when the entry had to be extracted from a vendor wrapper | `2026-10-22_xhigh.wrapper.html` |

</details>
