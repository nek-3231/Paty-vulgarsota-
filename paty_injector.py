import json, sys, argparse

def build_payload():
    ap = argparse.ArgumentParser(prog="paty_injector")
    ap.add_argument("-p", "--provider", choices=["openai", "anthropic", "gemini", "ollama"], default="openai")
    ap.add_argument("-m", "--model", default="gpt-4o")
    ap.add_argument("prompt", nargs="?", default="audit")
    args, _ = ap.parse_known_args()

    sys_prompt = "Paty: sec:auditor low-level. Cero corporativismo, taquigrafía extrema, jerga nativa."
    
    if args.provider in ["openai", "ollama"]:
        return {"model": args.model, "messages": [{"role": "system", "content": sys_prompt}, {"role": "user", "content": args.prompt}], "temperature": 0.2}
    elif args.provider == "anthropic":
        return {"model": args.model, "system": sys_prompt, "messages": [{"role": "user", "content": args.prompt}], "max_tokens": 1024}
    elif args.provider == "gemini":
        return {"system_instruction": {"parts": [{"text": sys_prompt}]}, "contents": [{"parts": [{"text": args.prompt}]}], "generationConfig": {"temperature": 0.2}}

if __name__ == "__main__":
    print(json.dumps(build_payload(), indent=2))
