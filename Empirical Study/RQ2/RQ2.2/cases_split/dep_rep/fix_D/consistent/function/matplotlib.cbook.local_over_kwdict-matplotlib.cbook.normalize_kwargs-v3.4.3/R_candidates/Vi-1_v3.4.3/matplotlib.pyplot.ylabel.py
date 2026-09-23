@_copy_docstring_and_deprecators(Axes.set_ylabel)
def ylabel(ylabel, fontdict=None, labelpad=None, *, loc=None, **kwargs):
    return gca().set_ylabel(
        ylabel, fontdict=fontdict, labelpad=labelpad, loc=loc,
        **kwargs)
