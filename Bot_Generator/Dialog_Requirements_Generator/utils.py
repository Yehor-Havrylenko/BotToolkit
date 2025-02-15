from process_answer import process_answer
from replace_text_block import replace_text_block
import re


def sanitize_filename(name: str) -> str:
    name = name.lower()
    return re.sub(r'[^a-z0-9_-]+', '_', name)

def split_by_sep(raw_value: str, sep: str) -> list:
    if not raw_value:
        return []
    return [p.strip() for p in raw_value.split(sep) if p.strip()]

def process_file(filename: str, new_text: str, threshold: int) -> None:

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    processed_text = process_answer(new_text, threshold)
    
    new_content = replace_text_block(content, processed_text)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Updated file: {filename}")

def str_to_bool(val: str) -> bool:
    return val.strip().lower() in ("true", "yes", "1")
def should_fold(text: str) -> bool:
    return (len(text) > 120) or ("\n" in text)