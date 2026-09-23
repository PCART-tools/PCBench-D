def _arg_slen1(dvi, delta):
    """
    Read *delta*+1 bytes, returning the bytes interpreted as signed.
    """
    return dvi._arg(delta + 1, True)
