import re


WHITESPACE_RE = re.compile(r"\s+")



def normalize_text(text: str) -> str:
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [WHITESPACE_RE.sub(" ", line).strip() for line in cleaned.split("\n")]
    non_empty = [line for line in lines if line]
    return "\n".join(non_empty).strip()
