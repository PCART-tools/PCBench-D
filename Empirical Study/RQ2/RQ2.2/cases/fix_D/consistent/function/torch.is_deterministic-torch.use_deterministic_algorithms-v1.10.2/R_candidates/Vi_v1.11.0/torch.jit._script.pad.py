def pad(s: str, padding: int, offset: int = 0, char: str = ' '):
    if padding >= len(s):
        padding -= len(s)
    return ''.join([char for _ in range(padding + offset)]) + s
