@_copy_docstring_and_deprecators(Axes.set_xlabel)
def xlabel(xlabel, fontdict=None, labelpad=None, *, loc=None, **kwargs):
    return gca().set_xlabel(
        xlabel, fontdict=fontdict, labelpad=labelpad, loc=loc,
        **kwargs)
