@_copy_docstring_and_deprecators(Axes.axhline)
def axhline(y=0, xmin=0, xmax=1, **kwargs):
    return gca().axhline(y=y, xmin=xmin, xmax=xmax, **kwargs)
