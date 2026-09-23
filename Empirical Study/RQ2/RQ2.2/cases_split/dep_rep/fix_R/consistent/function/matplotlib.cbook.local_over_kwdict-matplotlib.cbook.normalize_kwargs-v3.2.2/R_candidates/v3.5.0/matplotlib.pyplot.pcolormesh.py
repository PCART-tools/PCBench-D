@_copy_docstring_and_deprecators(Axes.pcolormesh)
def pcolormesh(
        *args, alpha=None, norm=None, cmap=None, vmin=None,
        vmax=None, shading=None, antialiased=False, data=None,
        **kwargs):
    __ret = gca().pcolormesh(
        *args, alpha=alpha, norm=norm, cmap=cmap, vmin=vmin,
        vmax=vmax, shading=shading, antialiased=antialiased,
        **({"data": data} if data is not None else {}), **kwargs)
    sci(__ret)
    return __ret
