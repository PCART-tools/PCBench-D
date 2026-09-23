def _arg_slen(dvi, delta):
    """
    Signed, length *delta*

    Read *delta* bytes, returning None if *delta* is zero, and the bytes
    interpreted as a signed integer otherwise.
    """
    if delta == 0:
        return None
    return dvi._arg(delta, True)
