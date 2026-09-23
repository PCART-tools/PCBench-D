@_copy_docstring_and_deprecators(Axes.tick_params)
def tick_params(axis='both', **kwargs):
    return gca().tick_params(axis=axis, **kwargs)
