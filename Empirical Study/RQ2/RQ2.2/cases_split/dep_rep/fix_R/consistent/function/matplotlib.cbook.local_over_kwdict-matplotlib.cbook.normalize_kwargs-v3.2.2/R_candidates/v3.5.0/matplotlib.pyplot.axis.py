@_copy_docstring_and_deprecators(Axes.axis)
def axis(*args, emit=True, **kwargs):
    return gca().axis(*args, emit=emit, **kwargs)
