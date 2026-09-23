def is_close_to_int(x, *, atol=1e-10):
    return abs(x - np.round(x)) < atol
