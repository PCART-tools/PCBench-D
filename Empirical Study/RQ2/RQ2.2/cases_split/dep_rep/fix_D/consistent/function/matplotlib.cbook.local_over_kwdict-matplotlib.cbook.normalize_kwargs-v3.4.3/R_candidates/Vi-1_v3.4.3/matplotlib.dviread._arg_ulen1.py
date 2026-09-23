def _arg_ulen1(dvi, delta):
    """
    Unsigned length *delta*+1

    Read *delta*+1 bytes, returning the bytes interpreted as unsigned.
    """
    return dvi._arg(delta+1, False)
