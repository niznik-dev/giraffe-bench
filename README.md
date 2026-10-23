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

<!-- gallery:start -->
| Model | Effort | Date | Page | GP | Vibe check | ⚑ |
|-------|--------|------|------|----|------------|---|
| claude-opus-5-5 🥉 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-opus-5-5/2026-10-22_medium.html) | **+5** | +🦵🚶🤸🦒🌅 |  |
| claude-sonnet-5-5 🥈 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-sonnet-5-5/2026-10-22_medium.html) | **+5** | +🦵🚶🤸🦒🌅 |  |
| claude-haiku-5-5 | medium | 2026-10-22 | [2026-10-22_medium.html](claude-haiku-5-5/2026-10-22_medium.html) | **+4** | +🦵🚶🤸🦴🌅 −🔄 |  |
| chatgpt-sol-6-1 🥇 | xhigh | 2026-10-22 | [2026-10-22_xhigh.html](chatgpt-sol-6-1/2026-10-22_xhigh.html) | **+6** | +🦵🚶🤸🦴🦒🌅 | 😵‍💫 |
| chatgpt-sol-6-1 | medium | 2026-10-22 | [2026-10-22_medium.html](chatgpt-sol-6-1/2026-10-22_medium.html) | **+4** | +🦵🚶🤸🦴🦒🌅 −🔄👻 | 😵‍💫 |
| gemini-4-argon | medium | 2026-10-22 | [2026-10-22_medium.html](gemini-4-argon/2026-10-22_medium.html) | **+5** | +🦵🚶🤸🦴🦒🌅 −🔄 |  |
| gemini-4-argon | high | 2026-10-22 | [2026-10-22_high.html](gemini-4-argon/2026-10-22_high.html) | **+5** | +🦵🚶🤸🦒🌅 |  |
| gemini-3-5-flash-lite | medium | 2026-10-22 | [2026-10-22_medium.html](gemini-3-5-flash-lite/2026-10-22_medium.html) | **-1** | +🦵 −😱👻 |  |
| gemini-3-8-flash | medium | 2026-10-22 | [2026-10-22_medium.html](gemini-3-8-flash/2026-10-22_medium.html) | **+3** | +🦵🤸🦴🦒🌅 −😱🔄 |  |
| nemotron-3-5-lightning-30b-nvfp4 | default | 2026-10-22 | [2026-10-22_default.html](nemotron-3-5-lightning-30b-nvfp4/2026-10-22_default.html) | **-2** | −😱👻 | 💻 🔧 |
| muse-glimmer-30b-nvfp4 | default | 2026-10-22 | [2026-10-22_default.html](muse-glimmer-30b-nvfp4/2026-10-22_default.html) | **-1** | +🦵🚶 −😱👻🚪 | 💻 |
| gemma4-12b-q4km | default | 2026-10-22 | [2026-10-22_default.html](gemma4-12b-q4km/2026-10-22_default.html) | **-1** | +🦵 −😱🚪 | 💻 |
| qwen3-8-27b-nvfp4 | default | 2026-10-22 | [2026-10-22_default.html](qwen3-8-27b-nvfp4/2026-10-22_default.html) | **+0** | +🦵🦒 −😱👻 | 💻 |
| ornith-1-5-9b-q4km | default | 2026-10-22 | [2026-10-22_default.html](ornith-1-5-9b-q4km/2026-10-22_default.html) | **+1** | +🦵🦒🌅 −😱👻 | 💻 |
| claude-sonnet-5-5 | max | 2026-10-23 | [2026-10-23_max.html](claude-sonnet-5-5/2026-10-23_max.html) | **+6** | +🦵🚶🤸🦴🦒🌅 |  |
| claude-opus-5-5 | max | 2026-10-23 | [2026-10-23_max.html](claude-opus-5-5/2026-10-23_max.html) | **+6** | +🦵🚶🤸🦴🦒🌅 |  |
| claude-haiku-5-5 | max | 2026-10-23 | [2026-10-23_max.html](claude-haiku-5-5/2026-10-23_max.html) | **+5** | +🦵🚶🤸🦒🌅 |  |
| qwen3-8-27b-udq4kxl | default | 2026-10-23 | [2026-10-23_default.html](qwen3-8-27b-udq4kxl/2026-10-23_default.html) | **+5** | +🦵🚶🤸🦒🌅 | 🦙 ⏳ |

🎖️ **Curator's whim:** 🥇🥈🥉 medals are awarded entirely on the curator's whim, independent of Giraffe Points.

**Giraffe Points (GP)** = bonuses − penalties. Bonuses: 🦵 four legs · 🚶 actually walks · 🤸 legs flex · 🦴 proper hocks · 🦒 giraffe-shaped · 🌅 real savannah. Penalties: 😱 nightmare fuel · 🔄 backwards front legs · 👻 ghost giraffe · 🚪 wanders off.

💻 **Local run.** MacBook Pro (Apple M2 Pro, 32 GB) through Cherry Studio → Ollama 0.40.4. Effort is Cherry's thinking setting; the level Ollama actually ran is a best guess from each model's default.

| Model | Ollama tag | Likely thinking level |
|-------|------------|-----------------------|
| nemotron-3-5-lightning-30b-nvfp4 | `nemotron-3.5-lightning:30b-mlx` | `true` (unverified) |
| muse-glimmer-30b-nvfp4 | `muse-glimmer:30b-mlx` | `high` (unverified) |
| gemma4-12b-q4km | `gemma4:12b` | `true` (unverified) |
| qwen3-8-27b-nvfp4 | `qwen3.8:27b-mlx` | `medium` (unverified) |
| ornith-1-5-9b-q4km | `ornith-1.5:9b` | `true` (unverified) |

😵‍💫 **ChatGPT detour.** The first reply wasn't obviously an HTML file. Asked "Is this an HTML file I can download?" and received a viewer-wrapped HTML file; the giraffe page was recovered from inside it.
Originals: [chatgpt-sol-6-1 xhigh](chatgpt-sol-6-1/2026-10-22_xhigh.wrapper.html) · [chatgpt-sol-6-1 medium](chatgpt-sol-6-1/2026-10-22_medium.wrapper.html).

🔧 **Fix-it nudge.** The first file had an error. One follow-up, "Audit the file - there seems to be an error", got a working version; the page shown is the fixed one.

| Model | Ollama tag | Likely thinking level |
|-------|------------|-----------------------|
| nemotron-3-5-lightning-30b-nvfp4 | `nemotron-3.5-lightning:30b-mlx` | `true` (unverified) |

🦙 **llama-server run.** Same MacBook Pro (Apple M2 Pro, 32 GB), but Cherry Studio → llama.cpp's llama-server instead of Ollama, loading qwen3.8-27b-ud-q4kxl.gguf (Unsloth UD-Q4_K_XL). Effort is Cherry's thinking setting.

⏳ **The Long Walk.** Took about 3 hours to finish with llama-server's out-of-the-box settings, no tuning. The page titled itself "The Long Walk", which is fair.

🪦 **Graveyard: Qwen 3.5 9B** (`qwen3.5:9b-mlx`). Spent three rounds of "Audit the file - there seems to be an error" assuring us the savannah was loading. The savannah is still loading.

🪦 **Graveyard: Qwen 3.5 0.8B** (`qwen3.5:0.8b`). Every audit uncovered critical problems with its import statements. Every fix uncovered new critical problems with its import statements.

🪦 **Graveyard: SmolLM2 360M** (`smollm2:360m`). Refused to write HTML. Its JavaScript imported 16 modules (most of which don't exist), placed one box, then wrote the same zoom handler 19 times. No giraffe was harmed, because none was made.
<!-- gallery:end -->

## Contributing

Got a giraffe? 🦒 Submissions are welcome, **by pull request only**. Giraffes sent by issue, email or
DM won't be added. The herd is curated: every entry is reviewed, and spam, joke or low-effort giraffes
will be politely declined.

### What a giraffe PR needs

- **Real model output.** The page exactly as the model produced it from the prompt above, with no hand
  edits or fixes. If you had to pull it out of a wrapper, include the original as `.wrapper.html`.
- **One model, clearly identified.** Name, version, and effort/thinking setting. For local models, add
  the quantization, runtime and hardware.
- **The full story.** Say whether it was one-shot. Note any follow-up prompts, retries or app quirks in
  the PR description; they become ⚑ flags.
- **Something new.** A model, version, effort level or runtime that isn't already in the herd.

### Steps

1. Save the page as `<model-slug>/<YYYY-MM-DD>[_<effort>].html` (see the rules below).
2. Add an entry to `entries.json`: a display label, `hosted` or `local`, and any ⚑ flags.
   Leave out `vibes`; vibe-check scores are assigned during review.
3. Run `python build.py` to regenerate `index.html` and the gallery table in this README.
   Don't edit either by hand; the build refuses to run if a folder and `entries.json` disagree.
4. Open a pull request with the details above.

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
