def get_tight_layout_figure(fig, axes_list, subplotspec_list, renderer,
                            pad=1.08, h_pad=None, w_pad=None, rect=None):
    """
    Return subplot parameters for tight-layouted-figure with specified padding.

    Parameters
    ----------
    fig : Figure
    axes_list : list of Axes
    subplotspec_list : list of `.SubplotSpec`
        The subplotspecs of each axes.
    renderer : renderer
    pad : float
        Padding between the figure edge and the edges of subplots, as a
        fraction of the font size.
    h_pad, w_pad : float
        Padding (height/width) between edges of adjacent subplots.  Defaults to
        *pad*.
    rect : tuple[float, float, float, float], optional
        (left, bottom, right, top) rectangle in normalized figure coordinates
        that the whole subplots area (including labels) will fit into.
        Defaults to using the entire figure.

    Returns
    -------
    subplotspec or None
        subplotspec kwargs to be passed to `.Figure.subplots_adjust` or
        None if tight_layout could not be accomplished.
    """

    subplot_list = []
    nrows_list = []
    ncols_list = []
    ax_bbox_list = []

    # Multiple axes can share same subplot_interface (e.g., axes_grid1); thus
    # we need to join them together.
    subplot_dict = {}

    subplotspec_list2 = []

    for ax, subplotspec in zip(axes_list, subplotspec_list):
        if subplotspec is None:
            continue

        subplots = subplot_dict.setdefault(subplotspec, [])

        if not subplots:
            myrows, mycols, _, _ = subplotspec.get_geometry()
            nrows_list.append(myrows)
            ncols_list.append(mycols)
            subplotspec_list2.append(subplotspec)
            subplot_list.append(subplots)
            ax_bbox_list.append(subplotspec.get_position(fig))

        subplots.append(ax)

    if len(nrows_list) == 0 or len(ncols_list) == 0:
        return {}

    max_nrows = max(nrows_list)
    max_ncols = max(ncols_list)

    num1num2_list = []
    for subplotspec in subplotspec_list2:
        rows, cols, num1, num2 = subplotspec.get_geometry()
        div_row, mod_row = divmod(max_nrows, rows)
        div_col, mod_col = divmod(max_ncols, cols)
        if mod_row != 0:
            _api.warn_external('tight_layout not applied: number of rows '
                               'in subplot specifications must be '
                               'multiples of one another.')
            return {}
        if mod_col != 0:
            _api.warn_external('tight_layout not applied: number of '
                               'columns in subplot specifications must be '
                               'multiples of one another.')
            return {}

        rowNum1, colNum1 = divmod(num1, cols)
        if num2 is None:
            rowNum2, colNum2 = rowNum1, colNum1
        else:
            rowNum2, colNum2 = divmod(num2, cols)

        num1num2_list.append((rowNum1 * div_row * max_ncols +
                              colNum1 * div_col,
                              ((rowNum2 + 1) * div_row - 1) * max_ncols +
                              (colNum2 + 1) * div_col - 1))

    kwargs = auto_adjust_subplotpars(fig, renderer,
                                     nrows_ncols=(max_nrows, max_ncols),
                                     num1num2_list=num1num2_list,
                                     subplot_list=subplot_list,
                                     ax_bbox_list=ax_bbox_list,
                                     pad=pad, h_pad=h_pad, w_pad=w_pad)

    # kwargs can be none if tight_layout fails...
    if rect is not None and kwargs is not None:
        # if rect is given, the whole subplots area (including
        # labels) will fit into the rect instead of the
        # figure. Note that the rect argument of
        # *auto_adjust_subplotpars* specify the area that will be
        # covered by the total area of axes.bbox. Thus we call
        # auto_adjust_subplotpars twice, where the second run
        # with adjusted rect parameters.

        left, bottom, right, top = rect
        if left is not None:
            left += kwargs["left"]
        if bottom is not None:
            bottom += kwargs["bottom"]
        if right is not None:
            right -= (1 - kwargs["right"])
        if top is not None:
            top -= (1 - kwargs["top"])

        kwargs = auto_adjust_subplotpars(fig, renderer,
                                         nrows_ncols=(max_nrows, max_ncols),
                                         num1num2_list=num1num2_list,
                                         subplot_list=subplot_list,
                                         ax_bbox_list=ax_bbox_list,
                                         pad=pad, h_pad=h_pad, w_pad=w_pad,
                                         rect=(left, bottom, right, top))

    return kwargs
