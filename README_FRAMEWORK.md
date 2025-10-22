# Supervisor Starter Pack (Full)

Drop this into your **repo template** to turn your orchestrator into a full-fledged agent
with judgment, memory, and guardrails.

## What’s inside
- `supervisor/`
  - `rules/` → policy, budgets, allowed paths, security
  - `prompts/` → preflight, validate, judge, forecast, final gate
  - `run.py` → JSON-in/JSON-out Supervisor (stub LLM; swap with your API)
  - `scripts/` → weekly learning loop (`aggregate_memory.py`, `retrain_policy.py`), logger
  - `memory.jsonl` → append-only memory log
- `.github/workflows/`
  - `00_supervisor.yml` → reusable workflow (workflow_call)
  - `01_plan.yml` → example: preflight + validate
  - `02_build.yml` → example: judge
  - `03_review.yml` → example: judge (re-run)
  - `04_qa.yml` → example: forecast
  - `05_gate.yml` → example: final gate
- `examples/handoff.json`

## How to use
1. Copy this pack into your template repo.
2. In your **real** plan/build/review/qa workflows, call:
   ```yaml
   - name: Supervisor Preflight
     uses: ./.github/workflows/00_supervisor.yml
     with: { mode: preflight }
   ```
   (valid modes: `preflight`, `validate`, `judge`, `forecast`, `gate`)

3. Log decisions:
   - Supervisor automatically appends decisions to `supervisor/memory.jsonl`.
   - You can also log manually: `python supervisor/scripts/log_decision.py '{"phase":"manual","verdict":"override","reason":"bench test OK"}'`

4. Weekly learning loop:
   ```bash
   python supervisor/scripts/aggregate_memory.py
   python supervisor/scripts/retrain_policy.py
   ```
   Review and merge the policy update PR.

## Swap in your LLMs
Open `supervisor/run.py` and replace `call_llm_stub` with your OpenAI/Anthropic calls.
Keep responses **JSON-only** to avoid parsing errors in CI.

Generated: 2025-10-20T17:34:53.456054Z
