# MVP Builder Template (Python + TypeScript) — Supervisor-ready

This template scaffolds a simple **device → parse → cloud** pipeline with both Python and TypeScript variants.
It is **wired to the Supervisor** reusable workflow you already added.

## Variants
- **Python**: Pydantic + simple adapters, pytest tests (stubs included)
- **TypeScript**: Zod + simple adapters, Vitest tests (stubs included)

## Quick Start
1. Ensure your repo already contains `.github/workflows/00_supervisor.yml` from the Supervisor Pack.
2. Use the workflows in `.github/workflows/10_mvp_plan.yml`, `11_mvp_build.yml`, `12_mvp_qa.yml` as references.
3. Edit `mvp/python/mvp.yaml` or `mvp/ts/mvp.yaml` to match your device and cloud endpoints.
4. Local run (Python):
   ```bash
   python -m mvp.python.main
   ```
   Local run (TypeScript):
   ```bash
   npm --prefix mvp/ts install
   npm --prefix mvp/ts run build
   node mvp/ts/dist/main.js
   ```

## Testing
- Python: add pytest config and run tests (`pytest`).
- TypeScript: `npm --prefix mvp/ts test`.

## Docker
- Python image: `mvp/python/infra/docker/Dockerfile`
- TypeScript image: `mvp/ts/infra/docker/Dockerfile`
- Compose files include Mosquitto and a mock cloud endpoint for quick e2e.

Generated: 2025-10-20T17:46:41.373506Z
