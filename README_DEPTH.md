# Supervisor Depth Upgrade Pack

Generated: 2025-10-22T20:26:58.901981Z

Adds a **depth** toggle so you can choose between **light** (cheap/fast) and **thorough** (GPT‑5‑Codex) per run.

## Files
- `supervisor/run.py` — accepts `--depth` and routes models accordingly. Supports OpenAI, Ollama, or stub fallback.
- `.github/workflows/00_supervisor.yml` — reusable workflow now accepts a `depth` input.
- `.github/workflows/01_plan_with_depth.yml` — example caller with a dropdown for depth.

## Env vars
- `OPENAI_API_KEY` (and optional `OPENAI_BASE_URL`)
- `OLLAMA_BASE_URL` (for local models, default `http://localhost:11434`)
- Optional overrides:
  - `SUPERVISOR_MODEL_LIGHT` (default `gpt-5-mini`)
  - `SUPERVISOR_MODEL_THOROUGH` (default `gpt-5-codex`)

## Usage
Trigger **agent-plan-with-depth** in Actions and select **light** or **thorough**.
Or call the reusable workflow from other jobs and pass `depth:` explicitly.
