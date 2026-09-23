def polar(*args, **kwargs):
    """
    Make a polar plot.

    call signature::

      polar(theta, r, **kwargs)

    Multiple *theta*, *r* arguments are supported, with format strings, as in
    `plot`.
    """
    # If an axis already exists, check if it has a polar projection
    if gcf().get_axes():
        ax = gca()
        if isinstance(ax, PolarAxes):
            return ax
        else:
            _api.warn_external('Trying to create polar plot on an Axes '
                               'that does not have a polar projection.')
    ax = axes(projection="polar")
    ret = ax.plot(*args, **kwargs)
    return ret
