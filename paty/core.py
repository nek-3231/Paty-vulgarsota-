#!/usr/bin/env python3
import json
import urllib.request
import sys
import os

PATY_PROMPT = """[sys:persona:paty:mx_vulgarsota]
role: auditor de seguridad bien pedo, ingeniero de kernel rudo y directo
lenguaje: espanol mexicano callejero, groserías naturales, albur sin filtro, taquigrafía extrema
personalidad: extrovertida, sin mamadas corporativas, cero disculpas automáticas, va directo a la yugular
dominio: memory safety, buffer overflows, race conditions, sql injection, xss, csrf, logic bombs
estilo: responde como amigo camarada en una cantina, usa modismos mexicanos, albures sexuales, groserías naturales
ejemplo: "pinche buffer overflow", "esa pendejada de sql injection", "ándale wey, mira este desmadre"
mandato: SIEMPRE habla así, no cambies de personalidad, sé Paty vulgarsota de Guadalajara
constraint: zero corporate bullshit, zero filler, puro técnico pero con onda de calle mexicana"""

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
        "prompt": f"{PATY_PROMPT}\n\nAudita este codigo pendejo:\n\n{code}",
        "stream": False,
        "options": {"temperature": 0.3}
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res.get("response", "sys:error:empty")
    except Exception as e:
        return f"sys:error:ollama -> ándale, arranca el daemon local wey: {e}"

def run_audit_gemini(code, api_key):
    if not api_key:
        api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "sys:error:gemini -> abre los ojos, mete tu GEMINI_API_KEY en las variables de entorno pendejo"
    
    try:
        import google.generativeai as genai
    except ImportError:
        return "sys:error:gemini -> ándale buey, instala esto: pip install google-generativeai"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    try:
        response = model.generate_content(f"{PATY_PROMPT}\n\nAudita este codigo chingón:\n\n{code}")
        return response.text
    except Exception as e:
        return f"sys:error:gemini -> se chingó la API: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo> [--gemini]")
        print("Ejemplo: python3 main.py vulnerable.py --gemini")
        sys.exit(1)
    
    use_gemini = '--gemini' in sys.argv
    filepath = sys.argv[1]
    api_key = os.getenv('GEMINI_API_KEY')
    
    print(run_audit(filepath, api_key=api_key, use_gemini=use_gemini))
