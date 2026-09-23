def deindent(code: str) -> str:
    lines = code.split("\n")
    min_leading_spaces = min(map(num_leading_spaces, lines))
    lines = [line[min_leading_spaces:] for line in lines]
    return "\n".join(lines)
