@_copy_docstring_and_deprecators(Axes.acorr)
def acorr(x, *, data=None, **kwargs):
    return gca().acorr(
        x, **({"data": data} if data is not None else {}), **kwargs)
