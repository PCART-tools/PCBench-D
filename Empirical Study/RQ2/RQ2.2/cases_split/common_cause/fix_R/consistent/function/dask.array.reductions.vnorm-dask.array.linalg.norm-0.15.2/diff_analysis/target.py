@wraps(np.linalg.norm)
def norm(x, ord=None, axis=None, keepdims=False):
    if x.ndim > 2:
        raise ValueError("Improper number of dimensions to norm.")

    if axis is None:
        axis = tuple(range(x.ndim))
    elif isinstance(axis, Number):
        axis = (int(axis),)
    else:
        axis = tuple(axis)

    if ord == "fro":
        ord = None
        if len(axis) == 1:
            raise ValueError("Invalid norm order for vectors.")

    # Coerce to double precision.
    r = x.astype(np.promote_types(x.dtype, float))

    if ord is None:
        r = (abs(r) ** 2).sum(axis=axis, keepdims=keepdims) ** 0.5
    elif ord == "nuc":
        if len(axis) == 1:
            raise ValueError("Invalid norm order for vectors.")

        r = svd(x)[1][None].sum(keepdims=keepdims)
    elif ord == np.inf:
        r = abs(r)
        if len(axis) == 1:
            r = r.max(axis=axis, keepdims=keepdims)
        else:
            r = r.sum(axis=axis[1], keepdims=keepdims).max(keepdims=keepdims)
    elif ord == -np.inf:
        r = abs(r)
        if len(axis) == 1:
            r = r.min(axis=axis, keepdims=keepdims)
        else:
            r = r.sum(axis=axis[1], keepdims=keepdims).min(keepdims=keepdims)
    elif ord == 0:
        if len(axis) == 2:
            raise ValueError("Invalid norm order for matrices.")

        r = (r != 0).astype(r.dtype).sum(axis=0, keepdims=keepdims)
    elif ord == 1:
        r = abs(r)
        if len(axis) == 1:
            r = r.sum(axis=axis, keepdims=keepdims)
        else:
            r = r.sum(axis=axis[0], keepdims=keepdims).max(keepdims=keepdims)
    elif len(axis) == 2 and ord == -1:
        r = abs(r).sum(axis=axis[0], keepdims=keepdims).min(keepdims=keepdims)
    elif len(axis) == 2 and ord == 2:
        r = svd(x)[1][None].max(keepdims=keepdims)
    elif len(axis) == 2 and ord == -2:
        r = svd(x)[1][None].min(keepdims=keepdims)
    else:
        if len(axis) == 2:
            raise ValueError("Invalid norm order for matrices.")

        r = (abs(r) ** ord).sum(axis=axis, keepdims=keepdims) ** (1.0 / ord)

    return r
