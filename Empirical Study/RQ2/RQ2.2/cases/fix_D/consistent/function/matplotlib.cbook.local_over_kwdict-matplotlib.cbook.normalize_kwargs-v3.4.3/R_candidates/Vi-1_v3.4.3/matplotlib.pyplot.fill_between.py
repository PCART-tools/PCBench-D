@_copy_docstring_and_deprecators(Axes.fill_between)
def fill_between(
        x, y1, y2=0, where=None, interpolate=False, step=None, *,
        data=None, **kwargs):
    return gca().fill_between(
        x, y1, y2=y2, where=where, interpolate=interpolate, step=step,
        **({"data": data} if data is not None else {}), **kwargs)
