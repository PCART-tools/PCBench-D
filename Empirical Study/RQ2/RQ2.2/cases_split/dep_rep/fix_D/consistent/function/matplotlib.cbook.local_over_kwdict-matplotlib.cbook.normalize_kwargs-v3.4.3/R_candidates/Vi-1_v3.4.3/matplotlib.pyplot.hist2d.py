@_copy_docstring_and_deprecators(Axes.hist2d)
def hist2d(
        x, y, bins=10, range=None, density=False, weights=None,
        cmin=None, cmax=None, *, data=None, **kwargs):
    __ret = gca().hist2d(
        x, y, bins=bins, range=range, density=density,
        weights=weights, cmin=cmin, cmax=cmax,
        **({"data": data} if data is not None else {}), **kwargs)
    sci(__ret[-1])
    return __ret
