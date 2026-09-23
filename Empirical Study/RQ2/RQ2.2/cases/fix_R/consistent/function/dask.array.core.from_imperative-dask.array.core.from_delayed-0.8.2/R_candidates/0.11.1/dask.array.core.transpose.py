@wraps(np.transpose)
def transpose(a, axes=None):
    axes = axes or tuple(range(a.ndim))[::-1]
    return atop(partial(np.transpose, axes=axes),
                axes,
                a, tuple(range(a.ndim)), dtype=a._dtype)
