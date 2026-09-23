def is_decade(x, base=10, *, rtol=1e-10):
    if not np.isfinite(x):
        return False
    if x == 0.0:
        return True
    lx = np.log(abs(x)) / np.log(base)
    return is_close_to_int(lx, atol=rtol)
