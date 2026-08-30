#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# arch:arm64:termux:net:scraper

import sys
import urllib.request
import urllib.parse
import json
import re

def web_query(query: str):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Linux; Android 11; Termux/Arch) AppleWebKit/537.36"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            snippets = re.findall(r'<a class="result__snippet[^>]*>(.*?)</a>', html, re.DOTALL)
            clean_res = [re.sub(r'<[^>]+>', '', s).strip() for s in snippets[:5]]
            return clean_res if clean_res else ["err:no:snippets:parsed"]
    except Exception as e:
        return [f"err:socket:fail:{str(e)}"]

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "kaist s3 lab"
    print(json.dumps(web_query(q), indent=2))
