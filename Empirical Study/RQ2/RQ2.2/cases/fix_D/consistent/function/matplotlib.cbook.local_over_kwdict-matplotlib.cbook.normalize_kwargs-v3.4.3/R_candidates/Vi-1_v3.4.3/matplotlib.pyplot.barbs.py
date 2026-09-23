@_copy_docstring_and_deprecators(Axes.barbs)
def barbs(*args, data=None, **kw):
    return gca().barbs(
        *args, **({"data": data} if data is not None else {}), **kw)
