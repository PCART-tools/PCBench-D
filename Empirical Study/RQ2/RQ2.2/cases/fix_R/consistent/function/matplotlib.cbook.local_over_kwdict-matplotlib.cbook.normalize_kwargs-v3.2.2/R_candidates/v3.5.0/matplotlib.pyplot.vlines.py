@_copy_docstring_and_deprecators(Axes.vlines)
def vlines(
        x, ymin, ymax, colors=None, linestyles='solid', label='', *,
        data=None, **kwargs):
    return gca().vlines(
        x, ymin, ymax, colors=colors, linestyles=linestyles,
        label=label, **({"data": data} if data is not None else {}),
        **kwargs)
