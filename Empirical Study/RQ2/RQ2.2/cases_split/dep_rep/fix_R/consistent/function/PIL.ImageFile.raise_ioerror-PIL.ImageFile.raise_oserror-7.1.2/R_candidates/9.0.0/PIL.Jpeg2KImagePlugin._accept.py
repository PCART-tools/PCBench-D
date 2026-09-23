def _accept(prefix):
    return (
        prefix[:4] == b"\xff\x4f\xff\x51"
        or prefix[:12] == b"\x00\x00\x00\x0cjP  \x0d\x0a\x87\x0a"
    )
