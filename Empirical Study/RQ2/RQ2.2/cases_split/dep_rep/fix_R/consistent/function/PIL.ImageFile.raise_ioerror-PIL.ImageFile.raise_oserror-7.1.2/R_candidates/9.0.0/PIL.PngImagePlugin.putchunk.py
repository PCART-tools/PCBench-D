def putchunk(fp, cid, *data):
    """Write a PNG chunk (including CRC field)"""

    data = b"".join(data)

    fp.write(o32(len(data)) + cid)
    fp.write(data)
    crc = _crc32(data, _crc32(cid))
    fp.write(o32(crc))
