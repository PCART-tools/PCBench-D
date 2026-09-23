@_copy_docstring_and_deprecators(Axes.margins)
def margins(*margins, x=None, y=None, tight=True):
    return gca().margins(*margins, x=x, y=y, tight=tight)
