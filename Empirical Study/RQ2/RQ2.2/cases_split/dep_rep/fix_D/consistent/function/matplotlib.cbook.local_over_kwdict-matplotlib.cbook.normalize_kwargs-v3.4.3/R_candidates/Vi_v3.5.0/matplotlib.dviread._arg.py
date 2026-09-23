def _arg(nbytes, signed, dvi, _):
    """
    Read *nbytes* bytes, returning the bytes interpreted as a signed integer
    if *signed* is true, unsigned otherwise.
    """
    return dvi._arg(nbytes, signed)
