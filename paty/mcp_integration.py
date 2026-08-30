#!/usr/bin/env python3
import os
import json
from paty.mcp_client import MCPClient

def collect_evidence(patterns=None, path="."):
    if patterns is None:
        patterns = ["vtable", "TOCTOU", "race", "memcpy", "memset", "message_header", "io_uring"]
    client = MCPClient()
    all_matches = []
    for p in patterns:
        try:
            res = client.send("rg.search", {"pattern": p, "path": path, "max_matches": 200}, timeout=15)
            if isinstance(res, dict) and "matches" in res:
                for m in res["matches"]:
                    all_matches.append({"pattern": p, **m})
        except Exception:
            continue
    client.close()
    return all_matches

def format_evidence(matches):
    lines = []
    for m in matches:
        lines.append(f"{m.get('pattern')} | {m.get('file')}:{m.get('line')} | {m.get('text')}")
    return "\\n".join(lines)

if __name__ == "__main__":
    target = "."
    matches = collect_evidence(path=target)
    print(json.dumps(matches, indent=2))
