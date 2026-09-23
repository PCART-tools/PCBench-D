@_copy_docstring_and_deprecators(Axes.annotate)
def annotate(text, xy, *args, **kwargs):
    return gca().annotate(text, xy, *args, **kwargs)
