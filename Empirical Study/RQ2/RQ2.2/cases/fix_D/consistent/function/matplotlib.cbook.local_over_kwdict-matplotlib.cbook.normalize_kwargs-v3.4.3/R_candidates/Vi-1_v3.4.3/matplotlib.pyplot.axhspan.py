@_copy_docstring_and_deprecators(Axes.axhspan)
def axhspan(ymin, ymax, xmin=0, xmax=1, **kwargs):
    return gca().axhspan(ymin, ymax, xmin=xmin, xmax=xmax, **kwargs)
