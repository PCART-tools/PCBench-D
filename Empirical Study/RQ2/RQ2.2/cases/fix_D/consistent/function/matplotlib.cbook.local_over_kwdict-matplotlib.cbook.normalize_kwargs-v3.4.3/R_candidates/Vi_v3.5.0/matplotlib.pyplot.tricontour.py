@_copy_docstring_and_deprecators(Axes.tricontour)
def tricontour(*args, **kwargs):
    __ret = gca().tricontour(*args, **kwargs)
    if __ret._A is not None: sci(__ret)  # noqa
    return __ret
