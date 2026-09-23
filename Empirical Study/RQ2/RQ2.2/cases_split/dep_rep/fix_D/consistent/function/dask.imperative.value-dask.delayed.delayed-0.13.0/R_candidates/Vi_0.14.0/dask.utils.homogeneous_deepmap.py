def homogeneous_deepmap(func, seq):
    if not seq:
        return seq
    n = 0
    tmp = seq
    while isinstance(tmp, list):
        n += 1
        tmp = tmp[0]

    return ndeepmap(n, func, seq)
