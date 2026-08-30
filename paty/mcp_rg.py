#!/usr/bin/env python3
import subprocess
import sys
import json

def search_code(query: str, path: str = "."):
    try:
        cmd = ["rg", "--json", "-i", query, path]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        results = []
        for line in res.stdout.splitlines():
            data = json.loads(line)
            if data.get("type") == "match":
                results.append({
                    "file": data["data"]["path"]["text"],
                    "line": data["data"]["line_number"],
                    "text": data["data"]["lines"]["text"].strip()
                })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def handle_rpc():
    for line in sys.stdin:
        try:
            req = json.loads(line)
            if req.get("method") == "tools/call":
                query = req["params"]["arguments"]["query"]
                res = search_code(query)
                sys.stdout.write(json.dumps({"jsonrpc": "2.0", "result": res, "id": req.get("id")}) + "\n")
                sys.stdout.flush()
        except Exception:
            pass

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        handle_rpc()
    else:
        query = sys.argv[1] if len(sys.argv) > 1 else ""
        if query:
            print(json.dumps(search_code(query), indent=2))
        else:
            print("Uso: python mcp_rg.py <patron> [--daemon]")
