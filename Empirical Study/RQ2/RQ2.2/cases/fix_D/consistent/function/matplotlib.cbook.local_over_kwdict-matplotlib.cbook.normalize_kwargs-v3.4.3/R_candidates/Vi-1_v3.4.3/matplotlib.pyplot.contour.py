@_copy_docstring_and_deprecators(Axes.contour)
def contour(*args, data=None, **kwargs):
    __ret = gca().contour(
        *args, **({"data": data} if data is not None else {}),
        **kwargs)
    if __ret._A is not None: sci(__ret)  # noqa
    return __ret
