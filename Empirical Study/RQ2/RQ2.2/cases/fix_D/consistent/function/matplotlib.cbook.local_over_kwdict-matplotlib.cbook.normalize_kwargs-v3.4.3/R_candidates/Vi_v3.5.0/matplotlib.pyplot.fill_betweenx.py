@_copy_docstring_and_deprecators(Axes.fill_betweenx)
def fill_betweenx(
        y, x1, x2=0, where=None, step=None, interpolate=False, *,
        data=None, **kwargs):
    return gca().fill_betweenx(
        y, x1, x2=x2, where=where, step=step, interpolate=interpolate,
        **({"data": data} if data is not None else {}), **kwargs)
