@_copy_docstring_and_deprecators(Axes.quiver)
def quiver(*args, data=None, **kw):
    __ret = gca().quiver(
        *args, **({"data": data} if data is not None else {}), **kw)
    sci(__ret)
    return __ret
