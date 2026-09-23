def si16le(c, o=0):
    """
    Converts a 2-bytes (16 bits) string to a signed integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """
    return unpack_from("<h", c, o)[0]
