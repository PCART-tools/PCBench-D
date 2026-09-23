@_copy_docstring_and_deprecators(Axes.axvline)
def axvline(x=0, ymin=0, ymax=1, **kwargs):
    return gca().axvline(x=x, ymin=ymin, ymax=ymax, **kwargs)
