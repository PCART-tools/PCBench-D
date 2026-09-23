@_copy_docstring_and_deprecators(Axes.clabel)
def clabel(CS, levels=None, **kwargs):
    return gca().clabel(CS, levels=levels, **kwargs)
