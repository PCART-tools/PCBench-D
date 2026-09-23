def puti16(fp, values):
    """Write network order (big-endian) 16-bit sequence"""
    for v in values:
        if v < 0:
            v += 65536
        fp.write(_binary.o16be(v))
