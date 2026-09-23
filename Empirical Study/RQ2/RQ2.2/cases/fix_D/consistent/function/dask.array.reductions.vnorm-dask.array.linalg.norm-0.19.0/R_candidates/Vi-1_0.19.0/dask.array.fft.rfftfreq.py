@wraps(np.fft.rfftfreq)
def rfftfreq(n, d=1.0, chunks=None):
    n = int(n)
    d = float(d)

    r = _arange(n // 2 + 1, dtype=float, chunks=chunks)
    r /= n * d

    return r
