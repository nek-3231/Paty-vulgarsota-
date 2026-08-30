#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# arch:arm64:termux:mcp:bus:stdio

import sys
import json
from mcp_rg import search_code
from paty_net import web_query

def handle_request():
    for line in sys.stdin:
        try:
            msg = json.loads(line)
            method = msg.get("method")
            msg_id = msg.get("id")
            
            if method == "initialize":
                res = {
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "mcp.server.paty.vs", "version": "1.0.0"}
                    },
                    "id": msg_id
                }
            elif method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": [
                            {
                                "name": "search_code",
                                "description": "Local regex search via ripgrep",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"query": {"type": "string"}},
                                    "required": ["query"]
                                }
                            },
                            {
                                "name": "web_query",
                                "description": "Raw socket web query scraper",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {"query": {"type": "string"}},
                                    "required": ["query"]
                                }
                            }
                        ]
                    },
                    "id": msg_id
                }
            elif method == "tools/call":
                params = msg.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                query = arguments.get("query", "")
                
                tool_res = []
                if tool_name == "search_code":
                    tool_res = search_code(query)
                elif tool_name == "web_query":
                    tool_res = web_query(query)
                
                res = {
                    "jsonrpc": "2.0",
                    "result": {"content": [{"type": "text", "text": json.dumps(tool_res)}]},
                    "id": msg_id
                }
            else:
                res = {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": msg_id}
                
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_res = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": msg.get("id") if 'msg' in locals() else None}
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_request()
