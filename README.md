# Paty-vulgarsota

⚠️ **Target:** Sec engineers / AI researchers. Local-first (Ollama/Llama3). Air-gapped mandatory. No cloud telemetry/egress.

## Phase 1: MVP Local

### Requirements
- Python 3.8+
- Ollama running locally (ollama serve)
- Llama3 model (ollama pull llama3)

### Installation
git clone https://github.com/nek-3231/Paty-vulgarsota-.git
cd Paty-vulgarsota-
pip install -r requirements.txt

### Quick Start
ollama serve &
python3 main.py examples/vulnerable.py
python3 verify_phase1.py examples/vulnerable.py
python3 tests/test_phase1.py

### Project Structure
paty/
__init__.py
core.py - Main audit engine
db.py - Local persistence
errors.py - Exception handling

tests/
test_phase1.py - Unit tests

examples/
vulnerable.py - Test sample

main.py - Entry point
verify_phase1.py - Phase 1 verification

### Features (Phase 1)
Local LLM inference (Ollama/Llama3)
File audit with system prompt
Local persistence (SQLite)
Error handling
Basic tests

### Environment Variables
PATY_MODEL=llama3
PATY_TEMP=0.1
PATY_OLLAMA_URL=http://localhost:11434

### Troubleshooting
sys:error:ollama_down - Start Ollama: ollama serve
sys:error:io - Check file path
sys:error:empty_response - Llama3 model not loaded

### TODO (Phase 2+)
Fine-tune Llama3 on CVE dataset
SAST integration (Semgrep, Bandit)
Multi-language support
CI/CD hooks
Web API

### License
MIT
