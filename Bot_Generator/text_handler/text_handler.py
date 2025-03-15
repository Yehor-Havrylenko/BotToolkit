#!/usr/bin/env python3
import os
import re
import sys
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.yaml")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def apply_replacements(text: str, replacements: list) -> str:
    for replacement in replacements:
        if isinstance(replacement, dict):
            for old, new in replacement.items():
                text = text.replace(old, new)

    text = text.strip("'\"")
    return text

def split_text_by_identifier(text: str, identifier: str):
    return text.split(identifier) if identifier in text else [text]

def process_answer(answer: str, base_indent: str, config: dict) -> str:
    text = answer.strip()
    text = apply_replacements(text, config.get("text_replacements", []))

    line_break_identifier = config.get("line_break_identifier", None)

    if line_break_identifier:
        text = text.replace("\\n", "\n")

    line_break_count = text.count("\n")
    split_lines = text.split("\n") if line_break_identifier else [text]

    formatted_lines = [f">-\n{base_indent}{base_indent}  {split_lines[0]}"]
    formatted_lines.extend(f"{base_indent}{base_indent}  {line.strip()}" for line in split_lines[1:])

    return "\n".join(formatted_lines)


def replace_text_blocks(content: str, config: dict) -> str:
    pattern = re.compile(r"^(\s*)(- text:\s*)(?!>-\s)(.*?)(?=\n\s*-\s|\n\s*\w+:|\Z)", re.MULTILINE | re.DOTALL)

    def repl(match):
        base_indent = match.group(1)
        text_prefix = match.group(2)
        text_value = match.group(3).strip()


        processed = process_answer(text_value, base_indent, config)
        return f"{base_indent}{text_prefix}{processed}"

    return pattern.sub(repl, content)


def process_file(filename: str, config: dict) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = replace_text_blocks(content, config)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated file: {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 text_handler.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    config = load_config()
    process_file(filename, config)

if __name__ == "__main__":
    main()
