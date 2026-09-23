def allclose(a, b, equal_nan=False, **kwargs):
    if getattr(a, 'dtype', None) != 'O':
        return np.allclose(a, b, equal_nan=equal_nan, **kwargs)
    if equal_nan:
        return (a.shape == b.shape and
                all(np.isnan(b) if np.isnan(a) else a == b
                    for (a, b) in zip(a.flat, b.flat)))
    return (a == b).all()
