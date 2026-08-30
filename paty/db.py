#!/usr/bin/env python3
import json
import os
from .errors import PatyDBError

DB_PATH = os.path.expanduser("~/.paty/audit_cache.json")

def init_db():
    """Inicializa la base de datos local"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w') as f:
            json.dump({"audits": []}, f)
    return True

def save_audit(filepath, result):
    """Guarda resultado de auditoría en caché local"""
    try:
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
        db["audits"].append({"file": filepath, "result": result})
        with open(DB_PATH, 'w') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        raise PatyDBError(f"Error guardando auditoría: {e}")

def get_audit(filepath):
    """Obtiene auditoría cacheada"""
    try:
        with open(DB_PATH, 'r') as f:
            db = json.load(f)
        for audit in db.get("audits", []):
            if audit["file"] == filepath:
                return audit["result"]
        return None
    except Exception as e:
        raise PatyDBError(f"Error leyendo caché: {e}")
