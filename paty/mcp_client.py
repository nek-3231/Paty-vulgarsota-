#!/usr/bin/env python3
import json
import subprocess
import threading
import queue
import time
import os

class MCPClient:
    def __init__(self, cmd=None):
        if cmd is None:
            cmd = ["python3", "-u", os.path.join(os.path.dirname(__file__), "mcp_daemon.py")]
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
        self._out_q = queue.Queue()
        self._reader = threading.Thread(target=self._reader_thread, daemon=True)
        self._reader.start()

    def _reader_thread(self):
        while True:
            line = self.proc.stdout.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            self._out_q.put(obj)

    def send(self, method, params=None, timeout=10.0):
        if params is None:
            params = {}
        req_id = int(time.time() * 1000)
        req = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}
        raw = json.dumps(req, separators=(",", ":"), ensure_ascii=False) + "\n"
        try:
            self.proc.stdin.write(raw)
            self.proc.stdin.flush()
        except Exception as e:
            raise RuntimeError(f"MCP send failed: {e}")
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                obj = self._out_q.get(timeout=0.1)
            except queue.Empty:
                continue
            if obj.get("id") == req_id:
                if "error" in obj:
                    raise RuntimeError(obj.get("error"))
                return obj.get("result")
        raise TimeoutError("MCP request timed out")

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass
        try:
            self.proc.wait(timeout=2)
        except Exception:
            pass
