#!/usr/bin/env python3
import json
import urllib.request
import sys

PATY_PROMPT = "[sys:persona:paty:vulgarsota] Auditor bajo nivel. Cero corporativismo, taquigrafía extrema, jerga nativa."

def inject_local(prompt="audit"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"{PATY_PROMPT}\n\n{prompt}",
        "stream": False
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print(json.dumps({
                "model": "llama3",
                "response": res.get("response", "")
            }, indent=2))
    except Exception as e:
        print(f"sys:error:ollama_down -> {e}")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "audit"
    inject_local(query)
