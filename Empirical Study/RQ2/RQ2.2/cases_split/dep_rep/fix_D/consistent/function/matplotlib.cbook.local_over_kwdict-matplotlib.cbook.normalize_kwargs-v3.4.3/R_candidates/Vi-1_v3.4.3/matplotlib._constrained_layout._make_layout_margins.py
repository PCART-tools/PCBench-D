def _make_layout_margins(fig, renderer, *, w_pad=0, h_pad=0,
                         hspace=0, wspace=0):
    """
    For each axes, make a margin between the *pos* layoutbox and the
    *axes* layoutbox be a minimum size that can accommodate the
    decorations on the axis.

    Then make room for colorbars.
    """
    for panel in fig.subfigs:  # recursively make child panel margins
        ss = panel._subplotspec
        _make_layout_margins(panel, renderer, w_pad=w_pad, h_pad=h_pad,
                             hspace=hspace, wspace=wspace)

        margins = _get_margin_from_padding(panel, w_pad=0, h_pad=0,
                                           hspace=hspace, wspace=wspace)
        panel._layoutgrid.parent.edit_outer_margin_mins(margins, ss)

    for ax in fig._localaxes.as_list():
        if not hasattr(ax, 'get_subplotspec') or not ax.get_in_layout():
            continue

        ss = ax.get_subplotspec()
        gs = ss.get_gridspec()
        nrows, ncols = gs.get_geometry()

        if gs._layoutgrid is None:
            return

        margin = _get_margin_from_padding(ax, w_pad=w_pad, h_pad=h_pad,
                                           hspace=hspace, wspace=wspace)
        margin0 = margin.copy()
        pos, bbox = _get_pos_and_bbox(ax, renderer)
        # the margin is the distance between the bounding box of the axes
        # and its position (plus the padding from above)
        margin['left'] += pos.x0 - bbox.x0
        margin['right'] += bbox.x1 - pos.x1
        # remember that rows are ordered from top:
        margin['bottom'] += pos.y0 - bbox.y0
        margin['top'] += bbox.y1 - pos.y1

        # make margin for colorbars.  These margins go in the
        # padding margin, versus the margin for axes decorators.
        for cbax in ax._colorbars:
            # note pad is a fraction of the parent width...
            pad = _colorbar_get_pad(cbax)
            # colorbars can be child of more than one subplot spec:
            cbp_rspan, cbp_cspan = _get_cb_parent_spans(cbax)
            loc = cbax._colorbar_info['location']
            cbpos, cbbbox = _get_pos_and_bbox(cbax, renderer)
            if loc == 'right':
                if cbp_cspan.stop == ss.colspan.stop:
                    # only increase if the colorbar is on the right edge
                    margin['rightcb'] += cbbbox.width + pad
            elif loc == 'left':
                if cbp_cspan.start == ss.colspan.start:
                    # only increase if the colorbar is on the left edge
                    margin['leftcb'] += cbbbox.width + pad
            elif loc == 'top':
                if cbp_rspan.start == ss.rowspan.start:
                    margin['topcb'] += cbbbox.height + pad
            else:
                if cbp_rspan.stop == ss.rowspan.stop:
                    margin['bottomcb'] += cbbbox.height + pad
            # If the colorbars are wider than the parent box in the
            # cross direction
            if loc in ['top', 'bottom']:
                if (cbp_cspan.start == ss.colspan.start and
                        cbbbox.x0 < bbox.x0):
                    margin['left'] += bbox.x0 - cbbbox.x0
                if (cbp_cspan.stop == ss.colspan.stop and
                        cbbbox.x1 > bbox.x1):
                    margin['right'] += cbbbox.x1 - bbox.x1
            # or taller:
            if loc in ['left', 'right']:
                if (cbp_rspan.stop == ss.rowspan.stop and
                        cbbbox.y0 < bbox.y0):
                    margin['bottom'] += bbox.y0 - cbbbox.y0
                if (cbp_rspan.start == ss.rowspan.start and
                        cbbbox.y1 > bbox.y1):
                    margin['top'] += cbbbox.y1 - bbox.y1
        # pass the new margins down to the layout grid for the solution...
        gs._layoutgrid.edit_outer_margin_mins(margin, ss)
