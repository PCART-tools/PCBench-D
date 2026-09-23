def _fftshift_helper(x, axes=None, inverse=False):
    if axes is None:
        axes = list(range(x.ndim))
    elif not isinstance(axes, Sequence):
        axes = (axes,)

    y = x
    for i in axes:
        n = y.shape[i]
        n_2 = (n + int(inverse is False)) // 2

        l = y.ndim * [slice(None)]
        l[i] = slice(None, n_2)
        l = tuple(l)

        r = y.ndim * [slice(None)]
        r[i] = slice(n_2, None)
        r = tuple(r)

        y = _concatenate([y[r], y[l]], axis=i)

        if len(x.chunks[i]) == 1:
            y = y.rechunk({i: x.chunks[i]})

    return y
