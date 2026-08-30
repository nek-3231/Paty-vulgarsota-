# Paty-vulgarsota

Auditor de seguridad local con Gemini, Ollama/Llama3. Air-gapped. Zero telemetry.

## Requisitos
- Python 3.8+
- Para Gemini: API key de Google
- Para Ollama: ollama serve + llama3

## Instalacion
git clone https://github.com/nek-3231/Paty-vulgarsota-.git
cd Paty-vulgarsota-
pip install -r requirements.txt

## Uso con Gemini
export GEMINI_API_KEY="tu-api-key-aqui"
python3 main.py archivo.py --gemini

## Uso con Ollama Local
ollama serve &
python3 main.py archivo.py

## Features
- Auditoria con Gemini o Llama3
- Cache local de resultados
- Deteccion de bugs, memory leaks, race conditions
- CLI simple

## Estructura
paty/
  core.py - Motor de auditoria
  db.py - Persistencia local
  errors.py - Excepciones

main.py - Entry point
