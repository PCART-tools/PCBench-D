def _extract_graph_and_keys(vals):
    """Given a list of dask vals, return a single graph and a list of keys such
    that ``get(dsk, keys)`` is equivalent to ``[v.compute() v in vals]``."""
    dsk = {}
    keys = []
    for v in vals:
        d = v.dask
        if type(d) is ShareDict:
            for dd in d.dicts.values():
                dsk.update(dd)
        else:
            dsk.update(v.dask)
        keys.append(v._keys())

    return dsk, keys
