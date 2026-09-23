@_copy_docstring_and_deprecators(Axes.arrow)
def arrow(x, y, dx, dy, **kwargs):
    return gca().arrow(x, y, dx, dy, **kwargs)
