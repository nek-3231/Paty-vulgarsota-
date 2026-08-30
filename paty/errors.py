#!/usr/bin/env python3

class PatyError(Exception):
    """Excepción base para Paty"""
    pass

class PatyFileError(PatyError):
    """Error al leer archivo"""
    pass

class PatyOllamaError(PatyError):
    """Error en conexión con Ollama"""
    pass

class PatyDBError(PatyError):
    """Error en base de datos"""
    pass
