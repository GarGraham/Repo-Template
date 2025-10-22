#!/usr/bin/env python3
# Utility to append an arbitrary decision/event to memory.jsonl
import sys, json, pathlib, datetime
m = pathlib.Path("supervisor/memory.jsonl")
m.parent.mkdir(parents=True, exist_ok=True)
entry = {"ts": datetime.datetime.utcnow().isoformat()+"Z"}
if len(sys.argv) > 1:
    entry.update(json.loads(sys.argv[1]))
with m.open("a", encoding="utf-8") as f:
    f.write(json.dumps(entry)+"\n")
print("Logged:", entry)
