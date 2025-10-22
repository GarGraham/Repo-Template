#!/usr/bin/env python3
import pathlib, datetime
draft = pathlib.Path("supervisor/policy_update_draft.md")
policy = pathlib.Path("supervisor/rules/policy.md")
if not draft.exists():
    print("No draft found; run aggregate_memory.py first."); raise SystemExit(0)
appendix = f"\n\n---\n\n_Last policy refresh: {datetime.datetime.utcnow().isoformat()}Z._\n"
policy.write_text(policy.read_text(encoding='utf-8') + appendix + draft.read_text(encoding='utf-8'), encoding='utf-8')
print("Appended draft to policy.md (open a PR with these changes).")
