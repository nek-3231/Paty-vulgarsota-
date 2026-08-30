#!/usr/bin/env python3
import sys
import json
import urllib.request

PATY_PROMPT = "[sys:persona:paty:mvp] Auditor bajo nivel. Cero rodeos, jerga técnica y calle. Detecta bugs de memoria, races y fallos de lógica."

def audit_file(filepath):
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except Exception as e:
        print(f"sys:error:file -> {e}")
        return

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"{PATY_PROMPT}\n\nAudita este código:\n\n{code}",
        "stream": False,
        "options": {"temperature": 0.1}
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            print(res.get("response", "sys:error:empty"))
    except Exception as e:
        print(f"sys:error:ollama -> arranca el daemon local: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 paty_core.py <archivo>")
        sys.exit(1)
    audit_file(sys.argv[1])
