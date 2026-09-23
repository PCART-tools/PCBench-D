@_copy_docstring_and_deprecators(Axes.tricontourf)
def tricontourf(*args, **kwargs):
    __ret = gca().tricontourf(*args, **kwargs)
    if __ret._A is not None: sci(__ret)  # noqa
    return __ret
