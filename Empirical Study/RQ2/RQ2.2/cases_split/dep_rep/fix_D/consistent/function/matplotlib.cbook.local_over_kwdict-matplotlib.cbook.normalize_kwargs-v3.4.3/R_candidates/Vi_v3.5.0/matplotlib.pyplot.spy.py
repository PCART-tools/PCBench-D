@_copy_docstring_and_deprecators(Axes.spy)
def spy(
        Z, precision=0, marker=None, markersize=None, aspect='equal',
        origin='upper', **kwargs):
    __ret = gca().spy(
        Z, precision=precision, marker=marker, markersize=markersize,
        aspect=aspect, origin=origin, **kwargs)
    if isinstance(__ret, cm.ScalarMappable): sci(__ret)  # noqa
    return __ret
