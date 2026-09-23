@_copy_docstring_and_deprecators(Axes.hexbin)
def hexbin(
        x, y, C=None, gridsize=100, bins=None, xscale='linear',
        yscale='linear', extent=None, cmap=None, norm=None, vmin=None,
        vmax=None, alpha=None, linewidths=None, edgecolors='face',
        reduce_C_function=np.mean, mincnt=None, marginals=False, *,
        data=None, **kwargs):
    __ret = gca().hexbin(
        x, y, C=C, gridsize=gridsize, bins=bins, xscale=xscale,
        yscale=yscale, extent=extent, cmap=cmap, norm=norm, vmin=vmin,
        vmax=vmax, alpha=alpha, linewidths=linewidths,
        edgecolors=edgecolors, reduce_C_function=reduce_C_function,
        mincnt=mincnt, marginals=marginals,
        **({"data": data} if data is not None else {}), **kwargs)
    sci(__ret)
    return __ret
