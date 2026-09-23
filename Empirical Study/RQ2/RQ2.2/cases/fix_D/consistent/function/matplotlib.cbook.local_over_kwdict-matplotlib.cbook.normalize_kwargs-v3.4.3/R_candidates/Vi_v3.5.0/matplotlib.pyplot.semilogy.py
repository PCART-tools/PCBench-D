@_copy_docstring_and_deprecators(Axes.semilogy)
def semilogy(*args, **kwargs):
    return gca().semilogy(*args, **kwargs)
