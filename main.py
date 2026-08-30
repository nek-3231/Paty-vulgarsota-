#!/usr/bin/env python3
import sys
import os
from paty.core import run_audit
from paty.db import init_db, save_audit

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <archivo> [--gemini]")
        sys.exit(1)
    
    use_gemini = '--gemini' in sys.argv
    filepath = sys.argv[1]
    
    try:
        init_db()
        api_key = os.getenv('GEMINI_API_KEY') if use_gemini else None
        result = run_audit(filepath, api_key=api_key, use_gemini=use_gemini)
        save_audit(filepath, result, model="gemini" if use_gemini else "llama3")
        print(result)
    except Exception as e:
        print(f"sys:err:crit -> {e}")
        sys.exit(1)
