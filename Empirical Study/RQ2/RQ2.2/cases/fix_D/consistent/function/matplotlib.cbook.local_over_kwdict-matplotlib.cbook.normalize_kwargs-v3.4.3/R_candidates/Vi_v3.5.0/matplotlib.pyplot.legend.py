@_copy_docstring_and_deprecators(Axes.legend)
def legend(*args, **kwargs):
    return gca().legend(*args, **kwargs)
