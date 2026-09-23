def argmax(seq, key=lambda x: x, start=0, end=None):
    seq = seq[start:end]
    if len(seq) == 0:
        return None
    return seq.index(max(seq, key=key)) + start
