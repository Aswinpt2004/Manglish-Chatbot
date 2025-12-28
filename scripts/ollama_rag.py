"""
Quick RAG-style chat via Ollama using WhatsApp pairs as context.
Requires: `pip install requests`

Run Ollama first and pull a small instruct model, e.g.:
  ollama pull llama3.2:3b-instruct
  ollama run llama3.2:3b-instruct

Usage:
  python scripts/ollama_rag.py --model llama3.2:3b-instruct
"""
import argparse
import json
import math
import os
from pathlib import Path
from typing import List, Dict, Any

import requests

DATA_IN = Path('data/processed/conversation_pairs.json')
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')


def load_pairs(path: Path) -> List[Dict[str, Any]]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def simple_retrieve(pairs: List[Dict[str, Any]], query: str, k: int = 3) -> List[str]:
    q_tokens = set(query.lower().split())
    scored = []
    for p in pairs:
        ctx = p.get('context', [])
        ctx_text = ' '.join(ctx) if isinstance(ctx, list) else str(ctx)
        tokens = set(ctx_text.lower().split())
        score = len(q_tokens & tokens) / (1 + math.log(1 + len(tokens)))
        scored.append((score, ctx_text, p.get('response', '')))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:k]
    # Return formatted context lines
    lines = []
    for _, ctx, resp in top:
        lines.append(f"User: {ctx}\nAssistant: {resp}")
    return lines


def chat_ollama(model: str, system: str, messages: List[Dict[str, str]]):
    url = f"{OLLAMA_URL}/api/chat"
    payload = {"model": model, "messages": messages, "stream": False}
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', default='llama3.2:3b-instruct')
    ap.add_argument('--k', type=int, default=3)
    args = ap.parse_args()

    if not DATA_IN.exists():
        raise FileNotFoundError("Missing data/processed/conversation_pairs.json. Run preprocess_whatsapp.py")

    pairs = load_pairs(DATA_IN)
    system = (
        "You are a Manglish assistant. Use short, friendly replies. "
        "If similar context is provided, mimic tone and style."
    )

    print("Type 'exit' to quit.\n")
    while True:
        try:
            user = input("You: ").strip()
            if user.lower() in {"exit", "quit", "bye"}:
                break
            ctx_lines = simple_retrieve(pairs, user, k=args.k)
            context_block = "\n\n".join(ctx_lines)
            prompt = (
                f"Here are similar past chats (for style/reference):\n\n{context_block}\n\n"
                f"Now answer the new user message in Manglish, concise."
            )
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
                {"role": "user", "content": user},
            ]
            reply = chat_ollama(args.model, system, messages)
            print(f"Bot: {reply}\n")
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
