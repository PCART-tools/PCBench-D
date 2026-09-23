@_copy_docstring_and_deprecators(Axes.pcolor)
def pcolor(
        *args, shading=None, alpha=None, norm=None, cmap=None,
        vmin=None, vmax=None, data=None, **kwargs):
    __ret = gca().pcolor(
        *args, shading=shading, alpha=alpha, norm=norm, cmap=cmap,
        vmin=vmin, vmax=vmax,
        **({"data": data} if data is not None else {}), **kwargs)
    sci(__ret)
    return __ret
