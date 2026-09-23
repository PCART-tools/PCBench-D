@_copy_docstring_and_deprecators(Axes.text)
def text(x, y, s, fontdict=None, **kwargs):
    return gca().text(x, y, s, fontdict=fontdict, **kwargs)
