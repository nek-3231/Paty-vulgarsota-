#!/usr/bin/env python3
import sys
from paty.core import run_audit
from paty.errors import PatyError

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo>")
        sys.exit(1)
    try:
        print(run_audit(sys.argv[1]))
    except PatyError as e:
        print(f"sys:err:crit -> {e}")
        sys.exit(1)
