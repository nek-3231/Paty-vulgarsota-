import json
import urllib.request
import urllib.error
import os
from paty.errors import OllamaOfflineError, AnalysisFailureError
from paty.db import save_audit
from paty.mcp_client import MCPClient

PATY_PROMPT = "[sys:persona:paty:prod] Auditor bajo nivel. Cero rodeos, jerga técnica y calle. Detecta bugs de memoria, races y fallos de lógica."

def gather_mcp_evidence(path="."):
    try:
        client = MCPClient()
        res = client.send("rg.search", {"pattern": "vtable|TOCTOU|race|memcpy|message_header|io_uring", "path": path, "max_matches": 200}, timeout=15)
        client.close()
        matches = res.get("matches", []) if isinstance(res, dict) else []
        evidence_lines = []
        for m in matches:
            evidence_lines.append(f\"{m.get('file')}:{m.get('line')}: {m.get('text')}\")
        return "\\n".join(evidence_lines)
    except Exception:
        return ""

def run_audit(filepath):
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except Exception as e:
        raise AnalysisFailureError(f"sys:error:io -> {e}")

    evidence = ""
    if os.getenv("PATY_BACKEND") == "mcp":
        evidence = gather_mcp_evidence(path=".")

    prompt_body = f"{PATY_PROMPT}\\n\\n"
    if evidence:
        prompt_body += f"EVIDENCE:\\n{evidence}\\n\\n"
    prompt_body += f"Audita este código:\\n\\n{code}"

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt_body,
        "stream": False,
        "options": {"temperature": 0.1}
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode('utf-8'))
            report = res.get("response", "")
            if not report:
                raise AnalysisFailureError("sys:error:empty_response")
            save_audit(filepath, report)
            return report
    except urllib.error.URLError as e:
        raise OllamaOfflineError(f"sys:error:ollama_down -> {e.reason}")
    except Exception as e:
        raise AnalysisFailureError(f\"sys:error:ollama -> {e}\")
