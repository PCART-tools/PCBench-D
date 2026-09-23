@wraps(np.transpose)
def transpose(a, axes=None):
    if axes:
        if len(axes) != a.ndim:
            raise ValueError("axes don't match array")
    else:
        axes = tuple(range(a.ndim))[::-1]
    axes = tuple(d + a.ndim if d < 0 else d for d in axes)
    return atop(np.transpose, axes, a, tuple(range(a.ndim)),
                dtype=a.dtype, axes=axes)
