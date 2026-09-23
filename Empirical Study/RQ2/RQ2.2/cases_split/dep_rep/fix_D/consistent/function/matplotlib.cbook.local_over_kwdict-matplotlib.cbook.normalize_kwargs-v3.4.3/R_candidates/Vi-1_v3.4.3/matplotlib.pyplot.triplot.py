@_copy_docstring_and_deprecators(Axes.triplot)
def triplot(*args, **kwargs):
    return gca().triplot(*args, **kwargs)
