import re


WHITESPACE_RE = re.compile(r"\s+")



def compact_whitespace(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value).strip()
