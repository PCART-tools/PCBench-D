def _check_no_collapsed_axes(fig):
    """
    Check that no axes have collapsed to zero size.
    """
    for panel in fig.subfigs:
        ok = _check_no_collapsed_axes(panel)
        if not ok:
            return False

    for ax in fig.axes:
        if hasattr(ax, 'get_subplotspec'):
            gs = ax.get_subplotspec().get_gridspec()
            lg = gs._layoutgrid
            if lg is not None:
                for i in range(gs.nrows):
                    for j in range(gs.ncols):
                        bb = lg.get_inner_bbox(i, j)
                        if bb.width <= 0 or bb.height <= 0:
                            return False
    return True
