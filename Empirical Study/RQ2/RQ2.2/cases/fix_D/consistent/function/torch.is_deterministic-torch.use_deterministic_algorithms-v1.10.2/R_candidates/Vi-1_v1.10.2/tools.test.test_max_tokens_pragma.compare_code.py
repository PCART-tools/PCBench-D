def compare_code(a: str, b: str) -> bool:
    a_lines = [line.strip() for line in a.splitlines()]
    b_lines = [line.strip() for line in b.splitlines()]
    return a_lines == b_lines
