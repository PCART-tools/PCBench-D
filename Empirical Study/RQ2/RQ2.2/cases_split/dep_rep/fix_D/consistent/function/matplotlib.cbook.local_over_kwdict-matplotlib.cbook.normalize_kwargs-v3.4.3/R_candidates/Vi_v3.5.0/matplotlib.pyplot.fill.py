@_copy_docstring_and_deprecators(Axes.fill)
def fill(*args, data=None, **kwargs):
    return gca().fill(
        *args, **({"data": data} if data is not None else {}),
        **kwargs)
