@_copy_docstring_and_deprecators(Axes.hlines)
def hlines(
        y, xmin, xmax, colors=None, linestyles='solid', label='', *,
        data=None, **kwargs):
    return gca().hlines(
        y, xmin, xmax, colors=colors, linestyles=linestyles,
        label=label, **({"data": data} if data is not None else {}),
        **kwargs)
