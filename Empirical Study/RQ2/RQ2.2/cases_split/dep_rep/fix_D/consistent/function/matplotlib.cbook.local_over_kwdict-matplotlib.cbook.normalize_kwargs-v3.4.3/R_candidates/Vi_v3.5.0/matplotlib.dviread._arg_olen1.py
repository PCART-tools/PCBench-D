def _arg_olen1(dvi, delta):
    """
    Read *delta*+1 bytes, returning the bytes interpreted as
    unsigned integer for 0<=*delta*<3 and signed if *delta*==3.
    """
    return dvi._arg(delta + 1, delta == 3)
