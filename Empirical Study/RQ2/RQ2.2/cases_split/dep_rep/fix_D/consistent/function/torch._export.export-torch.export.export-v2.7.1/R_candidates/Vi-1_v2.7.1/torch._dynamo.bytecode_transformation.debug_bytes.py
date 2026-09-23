def debug_bytes(*args) -> str:
    index = range(max(map(len, args)))
    result = [
        " ".join(f"{x:03}" for x in arg)
        for arg in [index]
        + list(args)
        + [[int(a != b) for a, b in zip(args[-1], args[-2])]]
    ]

    return "bytes mismatch\n" + "\n".join(result)
