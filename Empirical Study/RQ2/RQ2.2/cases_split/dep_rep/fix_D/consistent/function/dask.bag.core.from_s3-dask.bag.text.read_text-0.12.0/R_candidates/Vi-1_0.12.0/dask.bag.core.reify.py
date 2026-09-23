def reify(seq):
    if isinstance(seq, Iterator):
        seq = list(seq)
    if seq and isinstance(seq[0], Iterator):
        seq = list(map(list, seq))
    return seq
