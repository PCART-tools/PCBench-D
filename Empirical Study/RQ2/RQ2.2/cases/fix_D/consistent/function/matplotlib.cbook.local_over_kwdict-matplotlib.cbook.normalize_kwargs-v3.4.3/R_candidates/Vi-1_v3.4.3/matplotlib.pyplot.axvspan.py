@_copy_docstring_and_deprecators(Axes.axvspan)
def axvspan(xmin, xmax, ymin=0, ymax=1, **kwargs):
    return gca().axvspan(xmin, xmax, ymin=ymin, ymax=ymax, **kwargs)
