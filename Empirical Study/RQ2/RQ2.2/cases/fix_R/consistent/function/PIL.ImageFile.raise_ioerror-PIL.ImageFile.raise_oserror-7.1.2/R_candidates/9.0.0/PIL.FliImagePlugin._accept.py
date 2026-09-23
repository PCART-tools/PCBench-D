def _accept(prefix):
    return len(prefix) >= 6 and i16(prefix, 4) in [0xAF11, 0xAF12]
