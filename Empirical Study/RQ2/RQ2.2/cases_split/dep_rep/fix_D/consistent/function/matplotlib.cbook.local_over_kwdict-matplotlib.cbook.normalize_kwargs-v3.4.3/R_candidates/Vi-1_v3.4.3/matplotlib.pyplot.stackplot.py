@_copy_docstring_and_deprecators(Axes.stackplot)
def stackplot(
        x, *args, labels=(), colors=None, baseline='zero', data=None,
        **kwargs):
    return gca().stackplot(
        x, *args, labels=labels, colors=colors, baseline=baseline,
        **({"data": data} if data is not None else {}), **kwargs)
