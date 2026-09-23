def _remap_keys(m, f):
    m2 = {f(key): value for key, value in m.items()}
    m.clear()
    m.update(m2)
