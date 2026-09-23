@_copy_docstring_and_deprecators(Axes.contourf)
def contourf(*args, data=None, **kwargs):
    __ret = gca().contourf(
        *args, **({"data": data} if data is not None else {}),
        **kwargs)
    if __ret._A is not None: sci(__ret)  # noqa
    return __ret
