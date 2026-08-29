#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error

PATY_PROMPT = """
[sys:persona:paty:vulgarsota]
role: low-level security auditor & kernel engineer.
constraints: no corporate fluff, zero filler, raw street slang + precise technical jargon, extreme shorthand execution.
focus: memory safety, IPC, sandboxing, v8/mojo/gvisor/fuchsia internals.
"""

def query_ollama(prompt, model="llama3"):
    """
    ollama:local:exec -> Ejecución local gratuita, sin llamadas a nubes de terceros.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": f"{PATY_PROMPT}\n\nUser: {prompt}",
        "stream": False,
        "options": {"temperature": 0.1}
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get("response", "sys:error:empty_response")
    except urllib.error.URLError as e:
        return f"sys:error:ollama_offline -> levanta ollama localmente: {e.reason}"

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "analiza este volcado"
    print(query_ollama(query))
