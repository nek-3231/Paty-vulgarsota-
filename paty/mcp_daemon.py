#!/usr/bin/env python3
import sys
import json
import subprocess

def send_response(id_, result=None, error=None):
    resp = {"jsonrpc": "2.0", "id": id_}
    if error is not None:
        resp["error"] = {"message": str(error)}
    else:
        resp["result"] = result
    sys.stdout.write(json.dumps(resp, separators=(",", ":"), ensure_ascii=False) + "\n")
    sys.stdout.flush()

def handle_rg_search(params):
    pattern = params.get("pattern", "")
    path = params.get("path", ".")
    max_matches = int(params.get("max_matches", 200))
    try:
        cmd = ["rg", "--json", "-i", pattern, path]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        results = []
        for line in proc.stdout.splitlines():
            try:
                data = json.loads(line)
            except Exception:
                continue
            if data.get("type") == "match":
                results.append({
                    "file": data["data"]["path"]["text"],
                    "line": data["data"]["line_number"],
                    "text": data["data"]["lines"]["text"].strip()
                })
                if len(results) >= max_matches:
                    break
        return {"matches": results}
    except Exception as e:
        return {"error": str(e)}

def main():
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            req = json.loads(raw)
        except Exception:
            continue
        id_ = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        if method == "rg.search":
            res = handle_rg_search(params)
            if "error" in res:
                send_response(id_, error=res["error"])
            else:
                send_response(id_, result=res)
        else:
            send_response(id_, error=f"unsupported method {method}")

if __name__ == "__main__":
    main()
