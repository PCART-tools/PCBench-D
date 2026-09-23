def split(seq, n):
    """ Split apart a sequence into n equal pieces

    >>> split(range(10), 3)
    [[0, 1, 2], [3, 4, 5], [6, 7, 8, 9]]
    """
    if not isinstance(seq, (list, tuple)):
        seq = list(seq)

    part = len(seq) / n
    L = [seq[int(part * i): int(part * (i + 1))] for i in range(n - 1)]
    L.append(seq[int(part * (n - 1)):])
    return L
