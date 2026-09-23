def _accept(prefix):
    return len(prefix) >= 8 and i32(prefix, 0) >= 20 and i32(prefix, 4) in (1, 2)
