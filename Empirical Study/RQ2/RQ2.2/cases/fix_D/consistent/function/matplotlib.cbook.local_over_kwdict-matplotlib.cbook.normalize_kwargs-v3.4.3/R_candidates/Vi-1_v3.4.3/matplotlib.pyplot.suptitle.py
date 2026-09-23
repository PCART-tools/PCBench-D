@_copy_docstring_and_deprecators(Figure.suptitle)
def suptitle(t, **kwargs):
    return gcf().suptitle(t, **kwargs)
