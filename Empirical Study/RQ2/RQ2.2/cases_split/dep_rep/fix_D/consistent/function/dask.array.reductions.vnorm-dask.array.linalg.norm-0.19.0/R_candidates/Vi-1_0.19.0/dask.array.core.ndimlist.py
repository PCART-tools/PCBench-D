def ndimlist(seq):
    if not isinstance(seq, (list, tuple)):
        return 0
    elif not seq:
        return 1
    else:
        return 1 + ndimlist(seq[0])
