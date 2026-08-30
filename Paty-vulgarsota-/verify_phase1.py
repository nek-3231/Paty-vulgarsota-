#!/usr/bin/env python3
import sys
from paty.core import run_audit
from paty.db import init_db

def verify():
    print("sys:phase1:verify -> checking db & local inference pipeline...")
    init_db()
    print("sys:phase1:db -> ok")
    if len(sys.argv) > 1:
        print(f"sys:phase1:exec -> auditing target: {sys.argv[1]}")
        res = run_audit(sys.argv[1])
        print(res[:300] + "\n[... truncated ...]")
    else:
        print("sys:phase1:ready -> pasa un archivo objetivo para test de ejecución en vivo.")

if __name__ == "__main__":
    verify()
