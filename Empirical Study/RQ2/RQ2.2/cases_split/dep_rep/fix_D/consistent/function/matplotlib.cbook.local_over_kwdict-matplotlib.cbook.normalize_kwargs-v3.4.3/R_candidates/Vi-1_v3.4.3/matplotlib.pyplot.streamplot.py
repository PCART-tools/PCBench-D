@_copy_docstring_and_deprecators(Axes.streamplot)
def streamplot(
        x, y, u, v, density=1, linewidth=None, color=None, cmap=None,
        norm=None, arrowsize=1, arrowstyle='-|>', minlength=0.1,
        transform=None, zorder=None, start_points=None, maxlength=4.0,
        integration_direction='both', *, data=None):
    __ret = gca().streamplot(
        x, y, u, v, density=density, linewidth=linewidth, color=color,
        cmap=cmap, norm=norm, arrowsize=arrowsize,
        arrowstyle=arrowstyle, minlength=minlength,
        transform=transform, zorder=zorder, start_points=start_points,
        maxlength=maxlength,
        integration_direction=integration_direction,
        **({"data": data} if data is not None else {}))
    sci(__ret.lines)
    return __ret
