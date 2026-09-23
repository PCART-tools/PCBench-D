@_copy_docstring_and_deprecators(Axes.quiverkey)
def quiverkey(Q, X, Y, U, label, **kwargs):
    return gca().quiverkey(Q, X, Y, U, label, **kwargs)
