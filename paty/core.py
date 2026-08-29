import json
import urllib.request
import urllib.error
from paty.errors import OllamaOfflineError, AnalysisFailureError
from paty.db import save_audit

PATY_PROMPT = "[sys:persona:paty:prod] Auditor bajo nivel. Cero rodeos, jerga técnica y calle. Detecta bugs de memoria, races y fallos de lógica."

def run_audit(filepath):
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except Exception as e:
        raise AnalysisFailureError(f"sys:error:io -> {e}")

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
            report = res.get("response", "")
            if not report:
                raise AnalysisFailureError("sys:error:empty_response")
            save_audit(filepath, report)
            return report
    except urllib.error.URLError as e:
        raise OllamaOfflineError(f"sys:error:ollama_down -> {e.reason}")
