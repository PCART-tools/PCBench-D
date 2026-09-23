@_copy_docstring_and_deprecators(Axes.grid)
def grid(visible=None, which='major', axis='both', **kwargs):
    return gca().grid(visible=visible, which=which, axis=axis, **kwargs)
