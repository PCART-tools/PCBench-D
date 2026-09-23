def _fftfreq_block(i, n, d):
    r = i.copy()
    r[i >= (n + 1) // 2] -= n
    r /= n * d
    return r
