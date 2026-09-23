def _params(c=None, xsize=2, *, edgecolors=None, **kwargs):
    return (c, edgecolors, kwargs if kwargs is not None else {}, xsize)
