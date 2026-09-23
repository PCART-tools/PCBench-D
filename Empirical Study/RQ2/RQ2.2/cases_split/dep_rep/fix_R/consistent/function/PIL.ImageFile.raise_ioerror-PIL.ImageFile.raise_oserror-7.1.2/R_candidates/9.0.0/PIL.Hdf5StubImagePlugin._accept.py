def _accept(prefix):
    return prefix[:8] == b"\x89HDF\r\n\x1a\n"
