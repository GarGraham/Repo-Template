#!/usr/bin/env python3
import json, pathlib, collections, re, datetime

mem = pathlib.Path("supervisor/memory.jsonl")
out = pathlib.Path("supervisor/policy_update_draft.md")
clusters = collections.Counter()
hotspots = collections.Counter()

if mem.exists():
    for line in mem.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try:
            j=json.loads(line)
        except Exception:
            continue
        k=f"{j.get('phase','?')}:{j.get('verdict','?')}"
        clusters[k]+=1
        reason=(j.get('reason') or '').lower()
        for tok in re.findall(r"[a-z0-9_./-]{4,}", reason):
            if tok.startswith(("src/","app/","mvp/",".github/")):
                hotspots[tok]+=1

lines = ["# Weekly Supervisor Policy Draft",
         f"Generated: {datetime.datetime.utcnow().isoformat()}Z",
         "## Verdict Distribution"]
for k,v in clusters.most_common():
    lines.append(f"- {k}: {v}")
if hotspots:
    lines.append("\n## Hotspots")
    for k,v in hotspots.most_common(10):
        lines.append(f"- {k}: {v}")
lines += ["\n## Proposed Rules",
          "- Require golden fixtures for hotspot modules",
          "- Enforce rollback note + feature flag for user-visible changes",
          "- Tighten budgets where frequent revise/block occurs"]

out.write_text("\n".join(lines)+"\n", encoding="utf-8")
print(f"Wrote {out}")
