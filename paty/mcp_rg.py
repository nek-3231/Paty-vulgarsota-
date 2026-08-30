import sys

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

