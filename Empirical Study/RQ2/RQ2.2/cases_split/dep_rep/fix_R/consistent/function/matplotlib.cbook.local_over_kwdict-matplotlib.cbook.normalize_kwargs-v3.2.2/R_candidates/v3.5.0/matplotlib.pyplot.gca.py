@_copy_docstring_and_deprecators(Figure.gca)
def gca(**kwargs):
    return gcf().gca(**kwargs)
