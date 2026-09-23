@wraps(np.fft.fftfreq)
def fftfreq(n, d=1.0, chunks=None):
    n = int(n)
    d = float(d)

    r = _arange(n, dtype=float, chunks=chunks)

    return r.map_blocks(_fftfreq_block, dtype=float, n=n, d=d)
