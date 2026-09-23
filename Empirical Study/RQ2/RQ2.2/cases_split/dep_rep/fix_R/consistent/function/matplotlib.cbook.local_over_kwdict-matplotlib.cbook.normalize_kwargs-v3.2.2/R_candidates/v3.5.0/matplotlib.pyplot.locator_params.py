@_copy_docstring_and_deprecators(Axes.locator_params)
def locator_params(axis='both', tight=None, **kwargs):
    return gca().locator_params(axis=axis, tight=tight, **kwargs)
