def read_32t(fobj, start_length, size):
    # The 128x128 icon seems to have an extra header for some reason.
    (start, length) = start_length
    fobj.seek(start)
    sig = fobj.read(4)
    if sig != b"\x00\x00\x00\x00":
        raise SyntaxError("Unknown signature, expecting 0x00000000")
    return read_32(fobj, (start + 4, length - 4), size)
