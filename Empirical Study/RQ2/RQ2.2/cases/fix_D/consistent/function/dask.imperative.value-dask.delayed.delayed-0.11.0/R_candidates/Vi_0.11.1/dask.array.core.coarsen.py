@wraps(chunk.coarsen)
def coarsen(reduction, x, axes, trim_excess=False):
    if (not trim_excess and
        not all(bd % div == 0 for i, div in axes.items()
                for bd in x.chunks[i])):
        msg = "Coarsening factor does not align with block dimensions"
        raise ValueError(msg)

    if 'dask' in inspect.getfile(reduction):
        reduction = getattr(np, reduction.__name__)

    name = 'coarsen-' + tokenize(reduction, x, axes, trim_excess)
    dsk = dict(((name,) + key[1:], (chunk.coarsen, reduction, key, axes,
                                    trim_excess))
               for key in core.flatten(x._keys()))
    chunks = tuple(tuple(int(bd // axes.get(i, 1)) for bd in bds)
                   for i, bds in enumerate(x.chunks))

    if x._dtype is not None:
        dt = reduction(np.empty((1,) * x.ndim, dtype=x.dtype)).dtype
    else:
        dt = None
    return Array(merge(x.dask, dsk), name, chunks, dtype=dt)
