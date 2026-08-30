#!/usr/bin/env python3

class PatyError(Exception):
    pass

class PatyFileError(PatyError):
    pass

class PatyGeminiError(PatyError):
    pass

class PatyOllamaError(PatyError):
    pass

class PatyDBError(PatyError):
    pass
