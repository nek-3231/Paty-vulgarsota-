#!/usr/bin/env python3
import json
import urllib.request
import sys
import os

PATY_PROMPT = "[sys:persona:paty:mvp] Auditor bajo nivel. Cero rodeos, jerga tecnica y calle. Detecta bugs de memoria, races y fallos de logica."

def run_audit(filepath, api_key=None, use_gemini=False):
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except Exception as e:
        return f"sys:error:file -> {e}"
    
    if use_gemini:
        return run_audit_gemini(code, api_key)
    else:
        return run_audit_ollama(code)

def run_audit_ollama(code):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": f"{PATY_PROMPT}\n\nAudita este codigo:\n\n{code}",
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

def run_audit_gemini(code, api_key):
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "sys:error:gemini -> set GEMINI_API_KEY environment variable"
    
    try:
        import google.generativeai as genai
    except ImportError:
        return "sys:error:gemini -> install: pip install google-generativeai"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    try:
        response = model.generate_content(f"{PATY_PROMPT}\n\nAudita este codigo:\n\n{code}")
        return response.text
    except Exception as e:
        return f"sys:error:gemini -> {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 -m paty.core <archivo> [--gemini]")
        sys.exit(1)
    
    use_gemini = '--gemini' in sys.argv
    filepath = sys.argv[1]
    api_key = os.getenv('GEMINI_API_KEY')
    
    print(run_audit(filepath, api_key=api_key, use_gemini=use_gemini))
