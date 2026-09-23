@_copy_docstring_and_deprecators(Axes.imshow)
def imshow(
        X, cmap=None, norm=None, aspect=None, interpolation=None,
        alpha=None, vmin=None, vmax=None, origin=None, extent=None, *,
        filternorm=True, filterrad=4.0, resample=None, url=None,
        data=None, **kwargs):
    __ret = gca().imshow(
        X, cmap=cmap, norm=norm, aspect=aspect,
        interpolation=interpolation, alpha=alpha, vmin=vmin,
        vmax=vmax, origin=origin, extent=extent,
        filternorm=filternorm, filterrad=filterrad, resample=resample,
        url=url, **({"data": data} if data is not None else {}),
        **kwargs)
    sci(__ret)
    return __ret
