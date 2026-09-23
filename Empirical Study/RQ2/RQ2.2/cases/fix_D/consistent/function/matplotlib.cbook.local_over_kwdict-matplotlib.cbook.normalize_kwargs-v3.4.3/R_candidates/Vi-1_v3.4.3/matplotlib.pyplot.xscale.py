@_copy_docstring_and_deprecators(Axes.set_xscale)
def xscale(value, **kwargs):
    return gca().set_xscale(value, **kwargs)
