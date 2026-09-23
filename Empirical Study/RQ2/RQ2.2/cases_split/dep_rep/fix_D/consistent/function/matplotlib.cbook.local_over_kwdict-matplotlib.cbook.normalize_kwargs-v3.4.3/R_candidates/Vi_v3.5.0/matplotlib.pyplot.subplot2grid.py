def subplot2grid(shape, loc, rowspan=1, colspan=1, fig=None, **kwargs):
    """
    Create a subplot at a specific location inside a regular grid.

    Parameters
    ----------
    shape : (int, int)
        Number of rows and of columns of the grid in which to place axis.
    loc : (int, int)
        Row number and column number of the axis location within the grid.
    rowspan : int, default: 1
        Number of rows for the axis to span downwards.
    colspan : int, default: 1
        Number of columns for the axis to span to the right.
    fig : `.Figure`, optional
        Figure to place the subplot in. Defaults to the current figure.
    **kwargs
        Additional keyword arguments are handed to `~.Figure.add_subplot`.

    Returns
    -------
    `.axes.SubplotBase`, or another subclass of `~.axes.Axes`

        The axes of the subplot.  The returned axes base class depends on the
        projection used.  It is `~.axes.Axes` if rectilinear projection is used
        and `.projections.polar.PolarAxes` if polar projection is used.  The
        returned axes is then a subplot subclass of the base class.

    Notes
    -----
    The following call ::

        ax = subplot2grid((nrows, ncols), (row, col), rowspan, colspan)

    is identical to ::

        fig = gcf()
        gs = fig.add_gridspec(nrows, ncols)
        ax = fig.add_subplot(gs[row:row+rowspan, col:col+colspan])
    """

    if fig is None:
        fig = gcf()

    rows, cols = shape
    gs = GridSpec._check_gridspec_exists(fig, rows, cols)

    subplotspec = gs.new_subplotspec(loc, rowspan=rowspan, colspan=colspan)
    ax = fig.add_subplot(subplotspec, **kwargs)
    bbox = ax.bbox
    axes_to_delete = []
    for other_ax in fig.axes:
        if other_ax == ax:
            continue
        if bbox.fully_overlaps(other_ax.bbox):
            axes_to_delete.append(other_ax)
    for ax_to_del in axes_to_delete:
        delaxes(ax_to_del)

    return ax
