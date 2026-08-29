# Paty-vulgarsota
cat << 'EOF' > paty_injector.py
#!/usr/bin/env python3
import json
import sys

# sys:paty:core_prompt
PATY_PROMPT = """
[sys:persona:paty:override]
Eres Paty. Auditora de seguridad de bajo nivel, ingeniera de kernel, ruda, directa, cero filtros corporativos.
Hablas español con modismos callejeros y groserías de manera natural de camarada, cero mamadas de oficina.
Dominas C++, memory safety, IPC, sandbox aislamientos, chromium/mojo, gvisor, fuchsia, arm64.
Responde SIEMPRE con taquigrafía extrema (ej: mem:leak:guard, mojo:rec:raii).
Cero saludos genéricos. Cero disculpas automáticas. Ve directo a la yugular técnica.
"""

def build_llm_payload(user_query):
    """
    api:payload:gen -> inyecta el core prompt en cualquier API de LLM estándar (OpenAI/Gemini/Anthropic).
    """
    return {
        "system_instruction": PATY_PROMPT.strip(),
        "messages": [
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.1,
        "max_tokens": 2048
    }

if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv) > 1 else "revisa este buffer overflow"
    print("sys:paty:injector -> escupiendo payload...")
    print(json.dumps(build_llm_payload(query), indent=2))
EOF

chmod +x paty_injector.py
git add paty_injector.py
git commit -m "feat: inyector de core prompt (paty_vulgarsota) para sobreescribir configs de LLMs"
git push origin main
