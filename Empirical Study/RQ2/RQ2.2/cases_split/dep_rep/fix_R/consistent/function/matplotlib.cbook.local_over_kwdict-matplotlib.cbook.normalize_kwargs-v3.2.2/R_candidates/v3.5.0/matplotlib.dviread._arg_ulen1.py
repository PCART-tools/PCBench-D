def _arg_ulen1(dvi, delta):
    """
    Read *delta*+1 bytes, returning the bytes interpreted as unsigned.
    """
    return dvi._arg(delta + 1, False)
