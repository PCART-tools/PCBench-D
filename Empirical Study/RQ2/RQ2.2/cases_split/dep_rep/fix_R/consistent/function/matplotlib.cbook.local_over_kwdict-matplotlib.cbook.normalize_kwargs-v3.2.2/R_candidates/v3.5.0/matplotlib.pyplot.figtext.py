@_copy_docstring_and_deprecators(Figure.text)
def figtext(x, y, s, fontdict=None, **kwargs):
    return gcf().text(x, y, s, fontdict=fontdict, **kwargs)
