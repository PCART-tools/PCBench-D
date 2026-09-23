@_copy_docstring_and_deprecators(Axes.ticklabel_format)
def ticklabel_format(
        *, axis='both', style='', scilimits=None, useOffset=None,
        useLocale=None, useMathText=None):
    return gca().ticklabel_format(
        axis=axis, style=style, scilimits=scilimits,
        useOffset=useOffset, useLocale=useLocale,
        useMathText=useMathText)
