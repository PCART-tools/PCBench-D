def _crc32(data, seed=0):
    return zlib.crc32(data, seed) & 0xFFFFFFFF
