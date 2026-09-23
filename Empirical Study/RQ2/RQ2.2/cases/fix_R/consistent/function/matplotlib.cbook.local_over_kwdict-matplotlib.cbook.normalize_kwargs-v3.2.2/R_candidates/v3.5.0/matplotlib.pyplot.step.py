@_copy_docstring_and_deprecators(Axes.step)
def step(x, y, *args, where='pre', data=None, **kwargs):
    return gca().step(
        x, y, *args, where=where,
        **({"data": data} if data is not None else {}), **kwargs)
