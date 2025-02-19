import re
import sys
import textwrap

def process_answer(answer: str, base_indent: str, threshold: int = 60, wrap_width: int = 60) -> str:

    text = answer.strip()
    
    if len(text) >= 2 and ((text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'"))):
        text = text[1:-1].strip()
    
    text = text.replace('"', "'")

    if len(text) > threshold:
        wrapped_lines = textwrap.wrap(text, width=wrap_width)

        formatted_lines = [f">-\n{base_indent}{base_indent}  '{wrapped_lines[0]}"]
        formatted_lines.extend(f"{base_indent}{base_indent}  {line}" for line in wrapped_lines[1:])
        formatted_lines[-1] += "'"

        return "\n".join(formatted_lines)
    else:
        return f"'{text}'"  
    
def replace_text_blocks(content: str, threshold: int = 60) -> str:

    pattern = re.compile(r"^(\s*)(- text:\s*)(?!>-\s)([^\n]*)", re.MULTILINE)

    def repl(match):
        base_indent = match.group(1)  
        text_prefix = match.group(2) 
        text_value = match.group(3).strip() 

        if len(text_value) <= threshold:
            return f"{base_indent}{text_prefix}'{text_value}'"

        processed = process_answer(text_value, base_indent, threshold)

        return f"{base_indent}{text_prefix}{processed}"

    return pattern.sub(repl, content)

def process_file(filename: str, threshold: int = 60) -> None:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = replace_text_blocks(content, threshold)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated file: {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 process_file.py <filename> [threshold]")
        sys.exit(1)
    filename = sys.argv[1]
    try:
        threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    except ValueError:
        threshold = 60
    process_file(filename, threshold)

if __name__ == "__main__":
    main()
