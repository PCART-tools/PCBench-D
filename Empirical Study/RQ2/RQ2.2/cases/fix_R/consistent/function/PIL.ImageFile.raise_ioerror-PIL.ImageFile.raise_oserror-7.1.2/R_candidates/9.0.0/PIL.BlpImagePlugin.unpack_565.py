def unpack_565(i):
    return (((i >> 11) & 0x1F) << 3, ((i >> 5) & 0x3F) << 2, (i & 0x1F) << 3)
