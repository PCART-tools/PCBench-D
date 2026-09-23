@_copy_docstring_and_deprecators(Axes.barh)
def barh(y, width, height=0.8, left=None, *, align='center', **kwargs):
    return gca().barh(
        y, width, height=height, left=left, align=align, **kwargs)
