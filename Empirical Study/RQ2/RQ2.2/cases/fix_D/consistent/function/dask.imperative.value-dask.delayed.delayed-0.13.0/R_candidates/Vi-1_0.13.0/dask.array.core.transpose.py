@wraps(np.transpose)
def transpose(a, axes=None):
    if axes:
        if len(axes) != a.ndim:
            raise ValueError("axes don't match array")
    else:
        axes = tuple(range(a.ndim))[::-1]
    return atop(partial(np.transpose, axes=axes),
                axes,
                a, tuple(range(a.ndim)), dtype=a.dtype)
