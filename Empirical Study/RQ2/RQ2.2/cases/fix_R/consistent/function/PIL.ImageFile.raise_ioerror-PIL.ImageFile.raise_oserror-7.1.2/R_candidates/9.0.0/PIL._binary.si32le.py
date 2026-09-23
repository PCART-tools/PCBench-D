def si32le(c, o=0):
    """
    Converts a 4-bytes (32 bits) string to a signed integer.

    :param c: string containing bytes to convert
    :param o: offset of bytes to convert in string
    """
    return unpack_from("<i", c, o)[0]
