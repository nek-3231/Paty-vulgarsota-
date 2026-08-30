#!/usr/bin/env python3
import sys
from paty.core import run_audit
from paty.errors import PatyError
from paty.db import init_db, save_audit

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo>")
        sys.exit(1)
    try:
        init_db()
        result = run_audit(sys.argv[1])
        save_audit(sys.argv[1], result)
        print(result)
    except PatyError as e:
        print(f"sys:err:crit -> {e}")
        sys.exit(1)
