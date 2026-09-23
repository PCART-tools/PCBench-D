@_copy_docstring_and_deprecators(Axes.grid)
def grid(b=None, which='major', axis='both', **kwargs):
    return gca().grid(b=b, which=which, axis=axis, **kwargs)
