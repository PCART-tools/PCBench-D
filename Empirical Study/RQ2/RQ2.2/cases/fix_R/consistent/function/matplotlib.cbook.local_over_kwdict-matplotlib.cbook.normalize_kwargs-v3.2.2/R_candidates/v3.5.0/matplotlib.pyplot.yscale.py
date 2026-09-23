@_copy_docstring_and_deprecators(Axes.set_yscale)
def yscale(value, **kwargs):
    return gca().set_yscale(value, **kwargs)
