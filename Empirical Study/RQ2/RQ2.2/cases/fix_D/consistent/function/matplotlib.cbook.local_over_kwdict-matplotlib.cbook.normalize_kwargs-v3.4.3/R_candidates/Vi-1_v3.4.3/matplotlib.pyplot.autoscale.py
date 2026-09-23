@_copy_docstring_and_deprecators(Axes.autoscale)
def autoscale(enable=True, axis='both', tight=None):
    return gca().autoscale(enable=enable, axis=axis, tight=tight)
