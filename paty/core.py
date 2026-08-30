#!/usr/bin/env python3
import json
import urllib.request
import sys

PATY_PROMPT = "[sys:persona:paty:mvp] Auditor bajo nivel. Cero rodeos, jerga técnica y calle. Detecta bugs de memoria, races y fallos de lógica."

def run_audit(filepath):
    """Audita un archivo de código usando Ollama/Llama3 localmente"""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except Exception as e:
        return f"sys:error:file -> {e}"
    
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
            return res.get("response", "sys:error:empty")
    except Exception as e:
        return f"sys:error:ollama -> arranca el daemon local: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 -m paty.core <archivo>")
        sys.exit(1)
    print(run_audit(sys.argv[1]))
