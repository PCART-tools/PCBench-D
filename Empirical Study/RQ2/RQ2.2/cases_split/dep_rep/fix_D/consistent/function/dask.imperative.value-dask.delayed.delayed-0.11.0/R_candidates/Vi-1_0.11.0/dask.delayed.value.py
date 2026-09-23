def value(val, name=None):
    warn("``dask.imperative.value`` is renamed to ``delayed``")
    return delayed(val, name=name)
