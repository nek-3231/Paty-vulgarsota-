#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paty.db import init_db, save_audit, get_audit
from paty.errors import PatyError

def test_db_init():
    """Test: inicialización de BD"""
    try:
        init_db()
        print("✅ test_db_init passed")
        return True
    except Exception as e:
        print(f"❌ test_db_init failed: {e}")
        return False

def test_db_save_and_get():
    """Test: guardar y obtener auditoría"""
    try:
        init_db()
        save_audit("test.py", "sys:ok -> no vulnerabilities found")
        result = get_audit("test.py")
        assert result is not None
        print("✅ test_db_save_and_get passed")
        return True
    except Exception as e:
        print(f"❌ test_db_save_and_get failed: {e}")
        return False

if __name__ == "__main__":
    results = [
        test_db_init(),
        test_db_save_and_get()
    ]
    print(f"\n{sum(results)}/{len(results)} tests passed")
    sys.exit(0 if all(results) else 1)
