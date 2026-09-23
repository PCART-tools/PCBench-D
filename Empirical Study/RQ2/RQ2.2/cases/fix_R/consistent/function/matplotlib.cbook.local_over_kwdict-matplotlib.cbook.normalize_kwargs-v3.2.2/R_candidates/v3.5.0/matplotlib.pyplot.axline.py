@_copy_docstring_and_deprecators(Axes.axline)
def axline(xy1, xy2=None, *, slope=None, **kwargs):
    return gca().axline(xy1, xy2=xy2, slope=slope, **kwargs)
