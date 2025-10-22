#!/usr/bin/env python3
import os, json, sys, argparse, pathlib, datetime

# Swap this stub with a real LLM call (OpenAI, Anthropic, etc.). Keep JSON-only outputs.
def call_llm_stub(mode:str, content:str) -> dict:
    lower = (content or "").lower()
    verdict = "approve"
    reasons = []
    risk = 0.15
    sensitive = any(k in lower for k in ["schema","payment","auth","pii"])
    ambiguous = any(k in lower for k in ["todo","tbd","???","needs clar"])
    oversized = any(k in lower for k in ["massive","rewrite","monorepo"])
    if sensitive or ambiguous or oversized:
        verdict = "revise"
        if sensitive: reasons.append("Sensitive area detected — require split.")
        if ambiguous: reasons.append("Ambiguity detected — add AC.")
        if oversized: reasons.append("Scope likely exceeds budget — split into XS/S tasks.")
        risk = max(risk, 0.5 if sensitive else 0.35)
    return {"verdict": verdict, "reasons": reasons, "risk": risk}

def read_text(path):
    p = pathlib.Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""

def append_memory(entry):
    m = pathlib.Path("supervisor/memory.jsonl")
    m.parent.mkdir(parents=True, exist_ok=True)
    with m.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry)+"\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["preflight","validate","judge","forecast","gate"])
    ap.add_argument("--in", dest="infile", default="handoff.json")
    ap.add_argument("--out", dest="outfile", default="supervisor_out.json")
    args = ap.parse_args()

    now = datetime.datetime.utcnow().isoformat()+"Z"
    content = read_text(args.infile)
    res = call_llm_stub(args.mode, content)

    if args.mode == "preflight":
        out = {
            "verdict": res["verdict"],
            "reason": "; ".join(res["reasons"]) or "OK",
            "normalized_goal": "N/A (stub)",
            "constraints": ["budget: S", "paths: allowed"],
            "missing_info": [],
            "risk_score": res["risk"],
            "ts": now,
            "phase":"preflight"
        }
    elif args.mode == "validate":
        out = {
            "verdict": res["verdict"],
            "reason": "; ".join(res["reasons"]) or "OK",
            "required_splits": ["split-large-plan"] if res["verdict"]!="approve" else [],
            "required_tests": ["null/NaN boundaries"],
            "guardrails": ["no new deps without license check"],
            "ts": now,
            "phase":"validate"
        }
    elif args.mode == "judge":
        out = {
            "verdict": res["verdict"],
            "must_fix": ["add rollback note"] if res["verdict"]!="approve" else [],
            "nits": ["naming consistency"],
            "confidence": 0.72,
            "risk": res["risk"],
            "summary": ["Dual reviews reconciled", "No critical conflicts"],
            "ts": now,
            "phase":"judge"
        }
    elif args.mode == "forecast":
        out = {
            "cases": [
                {"name":"handles-null-sensor","type":"unit","desc":"Null/NaN handling in parser"},
                {"name":"e2e-happy-path","type":"e2e","desc":"Ingest → transform → emit works"}
            ],
            "required_fixtures": ["golden_ok.json","golden_bad.json"],
            "coverage_targets": {"lines": 0.8, "branches": 0.6},
            "verdict":"approve",
            "reason":"OK",
            "ts": now,
            "phase":"forecast"
        }
    else:  # gate
        out = {"verdict":"approve","reason":"All checks green","risk":0.2,"ts":now,"phase":"gate"}

    pathlib.Path(args.outfile).write_text(json.dumps(out, indent=2), encoding="utf-8")

    # Log to memory
    append_memory({
        "ts": now, "phase": out.get("phase"), "verdict": out.get("verdict"),
        "reason": out.get("reason", ""), "risk": out.get("risk", out.get("risk_score", None))
    })

if __name__ == "__main__":
    main()
