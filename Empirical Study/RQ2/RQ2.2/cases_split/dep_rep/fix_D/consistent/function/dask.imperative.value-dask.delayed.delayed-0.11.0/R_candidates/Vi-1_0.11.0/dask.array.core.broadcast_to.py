@wraps(chunk.broadcast_to)
def broadcast_to(x, shape):
    shape = tuple(shape)
    ndim_new = len(shape) - x.ndim
    if ndim_new < 0 or any(new != old
                           for new, old in zip(shape[ndim_new:], x.shape)
                           if old != 1):
        raise ValueError('cannot broadcast shape %s to shape %s'
                         % (x.shape, shape))

    name = 'broadcast_to-' + tokenize(x, shape)
    chunks = (tuple((s,) for s in shape[:ndim_new])
               + tuple(bd if old > 1 else (new,)
                       for bd, old, new in zip(x.chunks, x.shape,
                                               shape[ndim_new:])))
    dsk = dict(((name,) + (0,) * ndim_new + key[1:],
                (chunk.broadcast_to, key,
                 shape[:ndim_new] +
                 tuple(bd[i] for i, bd in zip(key[1:], chunks[ndim_new:]))))
               for key in core.flatten(x._keys()))
    return Array(merge(dsk, x.dask), name, chunks, dtype=x.dtype)
