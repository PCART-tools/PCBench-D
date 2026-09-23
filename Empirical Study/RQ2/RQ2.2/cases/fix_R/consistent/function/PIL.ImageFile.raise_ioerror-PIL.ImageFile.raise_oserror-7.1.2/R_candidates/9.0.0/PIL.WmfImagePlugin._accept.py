def _accept(prefix):
    return (
        prefix[:6] == b"\xd7\xcd\xc6\x9a\x00\x00" or prefix[:4] == b"\x01\x00\x00\x00"
    )
