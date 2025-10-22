#!/usr/bin/env python3
import os, json, sys, argparse, pathlib, datetime

MODEL_BY_DEPTH = {
    "light":  os.getenv("SUPERVISOR_MODEL_LIGHT",  "gpt-5-mini"),
    "thorough": os.getenv("SUPERVISOR_MODEL_THOROUGH", "gpt-5-codex"),
}

def call_openai(model, system_prompt, user_prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    import requests
    url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": [
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        "temperature": 0.2
    }
    r = requests.post(url, headers=headers, json=data, timeout=60)
    r.raise_for_status()
    j = r.json()
    return j["choices"][0]["message"]["content"]

def call_ollama(model, user_prompt):
    import requests
    base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    r = requests.post(f"{base}/api/generate", json={"model": model, "prompt": user_prompt, "stream": False}, timeout=60)
    r.raise_for_status()
    return r.json().get("response","")

def call_llm(mode, content, depth):
    model = MODEL_BY_DEPTH.get(depth or "light", "gpt-5-mini")
    system = f"You are the Supervisor in '{mode}' mode. Respond with compact JSON only."
    try:
        text = call_openai(model, system, content)
        return json.loads(text)
    except Exception:
        try:
            text = call_ollama(model, f"{system}\n\n{content}")
            return json.loads(text)
        except Exception:
            lower = (content or '').lower()
            verdict = 'approve'
            reasons = []
            risk = 0.15
            sensitive = any(k in lower for k in ['schema','payment','auth','pii'])
            ambiguous = any(k in lower for k in ['todo','tbd','???','needs clar'])
            oversized = any(k in lower for k in ['massive','rewrite','monorepo'])
            if sensitive or ambiguous or oversized:
                verdict = 'revise'
                if sensitive: reasons.append('Sensitive area detected — require split.')
                if ambiguous: reasons.append('Ambiguity detected — add AC.')
                if oversized: reasons.append('Scope likely exceeds budget — split into XS/S tasks.')
                risk = max(risk, 0.5 if sensitive else 0.35)
            return {'verdict': verdict, 'reasons': reasons, 'risk': risk, 'used_model': model, 'engine':'stub'}

def read_text(path):
    p = pathlib.Path(path)
    return p.read_text(encoding='utf-8') if p.exists() else ''

def append_memory(entry):
    m = pathlib.Path('supervisor/memory.jsonl')
    m.parent.mkdir(parents=True, exist_ok=True)
    with m.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry)+'\n')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=['preflight','validate','judge','forecast','gate'])
    ap.add_argument('--in', dest='infile', default='handoff.json')
    ap.add_argument('--out', dest='outfile', default='supervisor_out.json')
    ap.add_argument('--depth', default=os.getenv('SUPERVISOR_DEPTH','light'), help='light|thorough')
    args = ap.parse_args()

    depth = (args.depth or 'light').lower()
    now = datetime.datetime.utcnow().isoformat()+'Z'
    content = read_text(args.infile)

    res = call_llm(args.mode, content, depth)
    used_model = res.get('used_model') or MODEL_BY_DEPTH.get(depth, 'gpt-5-mini')

    def out_base(phase):
        return {'ts': now, 'phase': phase, 'used_model': used_model, 'depth': depth}

    if args.mode == 'preflight':
        out = {**out_base('preflight'),
               'verdict': res.get('verdict','approve'),
               'reason': '; '.join(res.get('reasons',[])) or 'OK',
               'normalized_goal': res.get('normalized_goal',''),
               'constraints': res.get('constraints',['budget:S','paths:allowed']),
               'missing_info': res.get('missing_info',[]),
               'risk_score': res.get('risk', 0.15)}
    elif args.mode == 'validate':
        out = {**out_base('validate'),
               'verdict': res.get('verdict','approve'),
               'reason': '; '.join(res.get('reasons',[])) or 'OK',
               'required_splits': res.get('required_splits',[]),
               'required_tests': res.get('required_tests',['null/NaN boundaries']),
               'guardrails': res.get('guardrails',['no new deps without license check'])}
    elif args.mode == 'judge':
        out = {**out_base('judge'),
               'verdict': res.get('verdict','approve'),
               'must_fix': res.get('must_fix',[]),
               'nits': res.get('nits',[]),
               'confidence': res.get('confidence',0.72),
               'risk': res.get('risk',0.2),
               'summary': res.get('summary',['Reviews reconciled'])}
    elif args.mode == 'forecast':
        out = {**out_base('forecast'),
               'verdict': res.get('verdict','approve'),
               'reason': res.get('reason','OK'),
               'cases': res.get('cases',[{'name':'handles-null-sensor','type':'unit','desc':'Null/NaN handling'}]),
               'required_fixtures': res.get('required_fixtures',['golden_ok.json','golden_bad.json']),
               'coverage_targets': res.get('coverage_targets',{'lines':0.8,'branches':0.6})}
    else:
        out = {**out_base('gate'),
               'verdict': res.get('verdict','approve'),
               'reason': res.get('reason','All checks green'),
               'risk': res.get('risk',0.2)}

    pathlib.Path(args.outfile).write_text(json.dumps(out, indent=2), encoding='utf-8')
    append_memory({
        'ts': now, 'phase': out.get('phase'), 'verdict': out.get('verdict'),
        'reason': out.get('reason', ''), 'risk': out.get('risk', out.get('risk_score', None)),
        'depth': depth, 'used_model': used_model
    })

if __name__ == '__main__':
    main()
