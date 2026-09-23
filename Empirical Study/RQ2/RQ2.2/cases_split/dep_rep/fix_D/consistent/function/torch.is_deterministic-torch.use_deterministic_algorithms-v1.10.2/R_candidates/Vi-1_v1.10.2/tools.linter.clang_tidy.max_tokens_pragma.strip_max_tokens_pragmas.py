def strip_max_tokens_pragmas(code: str) -> str:
    lines = code.splitlines()
    lines = [
        line
        for line in lines
        if re.match(MAX_TOKENS_PRAGMA_PATTERN, line.strip()) is None
    ]
    return "\n".join(lines)
