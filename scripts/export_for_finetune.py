"""
Export WhatsApp conversation pairs into common fine-tuning formats.

Inputs:
- data/processed/conversation_pairs.json (created by preprocess_whatsapp.py)

Outputs (under data/finetune/):
- openai_chat.jsonl     # OpenAI Chat-style JSONL (messages: system/user/assistant)
- sharegpt.jsonl        # LLaMA-Factory / ShareGPT-style
- alpaca_sft.jsonl      # Alpaca/Instruction-tuning style (instruction/input/output)
- train.jsonl / val.jsonl (OpenAI chat format split 95/5)

Usage:
  python scripts/export_for_finetune.py
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any

DATA_IN = Path('data/processed/conversation_pairs.json')
OUT_DIR = Path('data/finetune')
OUT_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM_PROMPT = (
    "You are a friendly Manglish (Malayalam+English) assistant. "
    "Answer briefly, natural, and colloquial."
)

def load_pairs(path: Path) -> List[Dict[str, Any]]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def to_openai_chat(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for p in pairs:
        context = p.get('context', [])
        context_text = ' | '.join(context) if isinstance(context, list) else str(context)
        response = p.get('response', '')
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": context_text},
            {"role": "assistant", "content": response},
        ]
        rows.append({"messages": messages})
    return rows


def to_sharegpt(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for p in pairs:
        context = p.get('context', [])
        context_text = ' | '.join(context) if isinstance(context, list) else str(context)
        response = p.get('response', '')
        rows.append({
            "conversations": [
                {"from": "system", "value": SYSTEM_PROMPT},
                {"from": "user", "value": context_text},
                {"from": "assistant", "value": response},
            ]
        })
    return rows


def to_alpaca(pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for p in pairs:
        context = p.get('context', [])
        context_text = ' | '.join(context) if isinstance(context, list) else str(context)
        response = p.get('response', '')
        rows.append({
            "instruction": "Reply in Manglish appropriately.",
            "input": context_text,
            "output": response,
        })
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, Any]]):
    with path.open('w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def split_train_val(rows: List[Dict[str, Any]], val_ratio: float = 0.05):
    n = len(rows)
    val_n = max(1, int(n * val_ratio))
    train = rows[:-val_n] if n > val_n else rows
    val = rows[-val_n:] if n > val_n else []
    return train, val


def main():
    if not DATA_IN.exists():
        raise FileNotFoundError(f"Missing {DATA_IN}. Run preprocess_whatsapp.py first.")

    pairs = load_pairs(DATA_IN)

    # OpenAI chat
    chat_rows = to_openai_chat(pairs)
    write_jsonl(OUT_DIR / 'openai_chat.jsonl', chat_rows)
    train, val = split_train_val(chat_rows)
    write_jsonl(OUT_DIR / 'train.jsonl', train)
    if val:
        write_jsonl(OUT_DIR / 'val.jsonl', val)

    # ShareGPT
    share_rows = to_sharegpt(pairs)
    write_jsonl(OUT_DIR / 'sharegpt.jsonl', share_rows)

    # Alpaca/Instruction
    alpaca_rows = to_alpaca(pairs)
    write_jsonl(OUT_DIR / 'alpaca_sft.jsonl', alpaca_rows)

    print("\n✅ Export complete!")
    print(f"- OpenAI Chat: {OUT_DIR / 'openai_chat.jsonl'}")
    print(f"- Train:       {OUT_DIR / 'train.jsonl'}")
    print(f"- Val:         {OUT_DIR / 'val.jsonl'}")
    print(f"- ShareGPT:    {OUT_DIR / 'sharegpt.jsonl'}")
    print(f"- Alpaca SFT:  {OUT_DIR / 'alpaca_sft.jsonl'}\n")


if __name__ == "__main__":
    main()
