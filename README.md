# project-template-aine

A boring-but-correct Python 3.11+ starter **with AI runtime pre-wired**. T1
(`project-template`) gives you a green lint+type+test gate on day 1; T2 adds
[`aine-platform`](https://github.com/fmonfasani/hookclose) so any new project
can call an LLM through one function call — and degrades to a deterministic
local fallback when no API key is set.

## What's in the box (beyond T1)

| Piece | Purpose |
|---|---|
| `pyproject.toml` | T1 + `aine-platform` dep + `pytest-asyncio` in dev extras |
| `src/{{ project_slug }}/ai/bootstrap.py` | `bootstrap_runtime()` → `AIBundle` (runtime + codegen). Optional injection of a custom `Runtime` for tests. |
| `scripts/ai_assist.py` | One-shot CLI: `python -m scripts.ai_assist "<goal>"` |
| `Makefile` `ai-task` target | `make ai-task GOAL="..."` |
| `.env.example` | `OPENROUTER_API_KEY`, `OPENROUTER_MODEL`, `OPENAI_API_KEY` |
| `tests/test_ai_bootstrap.py` | Pins the contract: fallback works with NO keys |
| `docs/AI.md` | How to mock providers in tests, where prompts live, cost notes |

Still no FastAPI / pydantic / Docker / WhatsApp / business vertical — that's
T3 (`whatsapp-sales-saas-template`) territory.

## Usage

```bash
# 1. Snapshot the template
npx degit fmonfasani/project-template-aine my-ai-project
cd my-ai-project

# 2. Fill placeholders + rename sample package
python scripts/init.py

# 3. Install + green-gate
make dev
make check

# 4. Try the AI surface (works without any keys -- uses local fallback)
make ai-task GOAL="write a fibonacci function"
```

To use a real provider, copy `.env.example` to `.env`, fill in
`OPENROUTER_API_KEY`, and re-run.

## What the AI runtime gives you

```python
from {{ project_slug }}.ai import bootstrap_runtime

bundle = bootstrap_runtime()
# bundle.runtime is an aine-platform Runtime with:
#   .providers    -- ProviderManager (routed completions)
#   .routing      -- ComplexityRoutingEngine (model selection by task)
#   .chainer      -- TaskChainer (multi-step workflows)
#   .healing      -- SelfHealingRuntime (retry / fallback)
# bundle.codegen is a CodeGenerator ready to turn goals into FilePatch[]
```

See [`docs/AI.md`](docs/AI.md) for details: mocking providers in tests,
prompt organization, cost ceilings.

## Day-to-day (inherited from T1)

```bash
make fmt        # ruff format + ruff --fix
make lint       # ruff check + ruff format --check
make type       # mypy --strict
make test       # pytest
make cov        # pytest + coverage report
make check      # lint + type + test (what CI runs)
make ai-task    # AI assistant (new in T2)
make clean      # nuke caches + build artifacts
```

## Why T2 exists (and isn't just `pip install aine-platform`)

Three things:

1. **One import path that won't change.** Re-exporting `bootstrap_runtime` /
   `codegen` / `AIBundle` from `{{ project_slug }}.ai` means your product code
   never references `runtime.composition` directly -- if `aine-platform`
   reshuffles its internal modules, you change exactly one file.
2. **Sane defaults out of the box.** A fresh project knows to read
   `OPENROUTER_API_KEY` from `.env`, knows how to mock providers in tests,
   knows where prompts go.
3. **Gate verde día 1, AI included.** `tests/test_ai_bootstrap.py` runs in CI
   from the first push, so a regression in the runtime wiring is caught
   before you've written a single feature.

## License

MIT (the template itself). The license of any project you generate from
the template is whatever you put in `scripts/init.py` -- defaults to MIT.
