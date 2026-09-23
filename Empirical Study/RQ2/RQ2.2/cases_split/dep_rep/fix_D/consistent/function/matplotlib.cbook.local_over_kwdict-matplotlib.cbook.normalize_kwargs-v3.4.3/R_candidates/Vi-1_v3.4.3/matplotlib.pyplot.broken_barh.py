@_copy_docstring_and_deprecators(Axes.broken_barh)
def broken_barh(xranges, yrange, *, data=None, **kwargs):
    return gca().broken_barh(
        xranges, yrange,
        **({"data": data} if data is not None else {}), **kwargs)
