#!/usr/bin/env python3
import json
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/.paty/audit_cache.json")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w') as f:
            json.dump({"audits": []}, f)
    return True

def save_audit(filepath, result, model="gemini"):
    try:
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
        db["audits"].append({"file": filepath, "result": result, "model": model, "timestamp": datetime.now().isoformat()})
        with open(DB_PATH, 'w') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        raise Exception(f"Error guardando auditoria: {e}")

def get_audit(filepath):
    try:
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
        for audit in db.get("audits", []):
            if audit["file"] == filepath:
                return audit["result"]
        return None
    except Exception as e:
        raise Exception(f"Error leyendo cache: {e}")
