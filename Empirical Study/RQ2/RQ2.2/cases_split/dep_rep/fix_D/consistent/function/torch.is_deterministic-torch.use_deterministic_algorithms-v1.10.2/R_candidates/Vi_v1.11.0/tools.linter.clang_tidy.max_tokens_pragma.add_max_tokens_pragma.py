def add_max_tokens_pragma(code: str, num_max_tokens: int) -> str:
    lines = code.splitlines()

    found_pragma = False
    pragma = f"#pragma clang max_tokens_total {num_max_tokens}"

    for idx, line in enumerate(lines):
        match = re.match(MAX_TOKENS_PRAGMA_PATTERN, line.strip())
        if match:
            found_pragma = True
            token_count = match.group(1)
            if int(token_count) != num_max_tokens:
                lines[idx] = pragma

    if not found_pragma:
        lines = [pragma] + lines

    return "\n".join(lines)
