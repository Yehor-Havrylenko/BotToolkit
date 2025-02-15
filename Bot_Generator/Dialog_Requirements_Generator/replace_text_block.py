import re

def replace_text_block(content: str, new_text: str) -> str:

    pattern = re.compile(r"^(\s*- text:\s*)(.*(?:\n(?:\s+.*))*)", re.MULTILINE)
    
    def repl(match):
        indent = match.group(1)
        return f"{indent}{new_text}"
    
    new_content = pattern.subn(repl, content, count=1)
    return new_content