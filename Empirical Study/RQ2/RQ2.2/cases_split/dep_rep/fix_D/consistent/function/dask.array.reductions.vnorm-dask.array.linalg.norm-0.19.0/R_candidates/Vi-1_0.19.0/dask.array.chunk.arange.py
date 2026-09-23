def arange(start, stop, step, length, dtype):
    res = np.arange(start, stop, step, dtype)
    return res[:-1] if len(res) > length else res
