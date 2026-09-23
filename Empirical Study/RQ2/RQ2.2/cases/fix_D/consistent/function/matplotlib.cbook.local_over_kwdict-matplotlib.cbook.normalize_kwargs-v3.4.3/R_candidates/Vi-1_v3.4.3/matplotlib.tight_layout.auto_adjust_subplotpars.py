def auto_adjust_subplotpars(
        fig, renderer, nrows_ncols, num1num2_list, subplot_list,
        ax_bbox_list=None, pad=1.08, h_pad=None, w_pad=None, rect=None):
    """
    Return a dict of subplot parameters to adjust spacing between subplots
    or ``None`` if resulting axes would have zero height or width.

    Note that this function ignores geometry information of subplot
    itself, but uses what is given by the *nrows_ncols* and *num1num2_list*
    parameters.  Also, the results could be incorrect if some subplots have
    ``adjustable=datalim``.

    Parameters
    ----------
    nrows_ncols : tuple[int, int]
        Number of rows and number of columns of the grid.
    num1num2_list : list[int]
        List of numbers specifying the area occupied by the subplot
    subplot_list : list of subplots
        List of subplots that will be used to calculate optimal subplot_params.
    pad : float
        Padding between the figure edge and the edges of subplots, as a
        fraction of the font size.
    h_pad, w_pad : float
        Padding (height/width) between edges of adjacent subplots, as a
        fraction of the font size.  Defaults to *pad*.
    rect : tuple[float, float, float, float]
        [left, bottom, right, top] in normalized (0, 1) figure coordinates.
    """
    rows, cols = nrows_ncols

    font_size_inches = (
        FontProperties(size=rcParams["font.size"]).get_size_in_points() / 72)
    pad_inches = pad * font_size_inches
    vpad_inches = h_pad * font_size_inches if h_pad is not None else pad_inches
    hpad_inches = w_pad * font_size_inches if w_pad is not None else pad_inches

    if len(num1num2_list) != len(subplot_list) or len(subplot_list) == 0:
        raise ValueError

    if rect is None:
        margin_left = margin_bottom = margin_right = margin_top = None
    else:
        margin_left, margin_bottom, _right, _top = rect
        margin_right = 1 - _right if _right else None
        margin_top = 1 - _top if _top else None

    vspaces = np.zeros((rows + 1, cols))
    hspaces = np.zeros((rows, cols + 1))

    if ax_bbox_list is None:
        ax_bbox_list = [
            Bbox.union([ax.get_position(original=True) for ax in subplots])
            for subplots in subplot_list]

    for subplots, ax_bbox, (num1, num2) in zip(subplot_list,
                                               ax_bbox_list,
                                               num1num2_list):
        if all(not ax.get_visible() for ax in subplots):
            continue

        bb = []
        for ax in subplots:
            if ax.get_visible():
                try:
                    bb += [ax.get_tightbbox(renderer, for_layout_only=True)]
                except TypeError:
                    bb += [ax.get_tightbbox(renderer)]

        tight_bbox_raw = Bbox.union(bb)
        tight_bbox = TransformedBbox(tight_bbox_raw,
                                     fig.transFigure.inverted())

        row1, col1 = divmod(num1, cols)
        if num2 is None:
            num2 = num1
        row2, col2 = divmod(num2, cols)

        for row_i in range(row1, row2 + 1):
            hspaces[row_i, col1] += ax_bbox.xmin - tight_bbox.xmin  # left
            hspaces[row_i, col2 + 1] += tight_bbox.xmax - ax_bbox.xmax  # right
        for col_i in range(col1, col2 + 1):
            vspaces[row1, col_i] += tight_bbox.ymax - ax_bbox.ymax  # top
            vspaces[row2 + 1, col_i] += ax_bbox.ymin - tight_bbox.ymin  # bot.

    fig_width_inch, fig_height_inch = fig.get_size_inches()

    # margins can be negative for axes with aspect applied, so use max(, 0) to
    # make them nonnegative.
    if not margin_left:
        margin_left = (max(hspaces[:, 0].max(), 0)
                       + pad_inches / fig_width_inch)
        suplabel = fig._supylabel
        if suplabel and suplabel.get_in_layout():
            rel_width = fig.transFigure.inverted().transform_bbox(
                suplabel.get_window_extent(renderer)).width
            margin_left += rel_width + pad_inches / fig_width_inch

    if not margin_right:
        margin_right = (max(hspaces[:, -1].max(), 0)
                        + pad_inches / fig_width_inch)
    if not margin_top:
        margin_top = (max(vspaces[0, :].max(), 0)
                      + pad_inches / fig_height_inch)
        if fig._suptitle and fig._suptitle.get_in_layout():
            rel_height = fig.transFigure.inverted().transform_bbox(
                fig._suptitle.get_window_extent(renderer)).height
            margin_top += rel_height + pad_inches / fig_height_inch
    if not margin_bottom:
        margin_bottom = (max(vspaces[-1, :].max(), 0)
                         + pad_inches / fig_height_inch)
        suplabel = fig._supxlabel
        if suplabel and suplabel.get_in_layout():
            rel_height = fig.transFigure.inverted().transform_bbox(
                suplabel.get_window_extent(renderer)).height
            margin_bottom += rel_height + pad_inches / fig_height_inch

    if margin_left + margin_right >= 1:
        _api.warn_external('Tight layout not applied. The left and right '
                           'margins cannot be made large enough to '
                           'accommodate all axes decorations. ')
        return None
    if margin_bottom + margin_top >= 1:
        _api.warn_external('Tight layout not applied. The bottom and top '
                           'margins cannot be made large enough to '
                           'accommodate all axes decorations. ')
        return None

    kwargs = dict(left=margin_left,
                  right=1 - margin_right,
                  bottom=margin_bottom,
                  top=1 - margin_top)

    if cols > 1:
        hspace = hspaces[:, 1:-1].max() + hpad_inches / fig_width_inch
        # axes widths:
        h_axes = (1 - margin_right - margin_left - hspace * (cols - 1)) / cols
        if h_axes < 0:
            _api.warn_external('Tight layout not applied. tight_layout '
                               'cannot make axes width small enough to '
                               'accommodate all axes decorations')
            return None
        else:
            kwargs["wspace"] = hspace / h_axes
    if rows > 1:
        vspace = vspaces[1:-1, :].max() + vpad_inches / fig_height_inch
        v_axes = (1 - margin_top - margin_bottom - vspace * (rows - 1)) / rows
        if v_axes < 0:
            _api.warn_external('Tight layout not applied. tight_layout '
                               'cannot make axes height small enough to '
                               'accommodate all axes decorations')
            return None
        else:
            kwargs["hspace"] = vspace / v_axes

    return kwargs
