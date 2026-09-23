@_copy_docstring_and_deprecators(Axes.bar)
def bar(
        x, height, width=0.8, bottom=None, *, align='center',
        data=None, **kwargs):
    return gca().bar(
        x, height, width=width, bottom=bottom, align=align,
        **({"data": data} if data is not None else {}), **kwargs)
