def _accept(prefix):
    return prefix[:4] == b"BUFR" or prefix[:4] == b"ZCZC"
