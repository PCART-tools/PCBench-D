@_copy_docstring_and_deprecators(Axes.scatter)
def scatter(
        x, y, s=None, c=None, marker=None, cmap=None, norm=None,
        vmin=None, vmax=None, alpha=None, linewidths=None, *,
        edgecolors=None, plotnonfinite=False, data=None, **kwargs):
    __ret = gca().scatter(
        x, y, s=s, c=c, marker=marker, cmap=cmap, norm=norm,
        vmin=vmin, vmax=vmax, alpha=alpha, linewidths=linewidths,
        edgecolors=edgecolors, plotnonfinite=plotnonfinite,
        **({"data": data} if data is not None else {}), **kwargs)
    sci(__ret)
    return __ret
