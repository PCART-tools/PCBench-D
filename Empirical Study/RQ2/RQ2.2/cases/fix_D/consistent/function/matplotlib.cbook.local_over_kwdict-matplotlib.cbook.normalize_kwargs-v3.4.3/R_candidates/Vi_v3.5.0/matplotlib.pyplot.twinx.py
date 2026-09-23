def twinx(ax=None):
    """
    Make and return a second axes that shares the *x*-axis.  The new axes will
    overlay *ax* (or the current axes if *ax* is *None*), and its ticks will be
    on the right.

    Examples
    --------
    :doc:`/gallery/subplots_axes_and_figures/two_scales`
    """
    if ax is None:
        ax = gca()
    ax1 = ax.twinx()
    return ax1
