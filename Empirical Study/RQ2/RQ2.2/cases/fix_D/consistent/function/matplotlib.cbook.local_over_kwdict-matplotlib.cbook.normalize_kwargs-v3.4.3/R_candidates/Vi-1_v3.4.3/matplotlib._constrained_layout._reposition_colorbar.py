def _reposition_colorbar(cbax, renderer, *, offset=None):
    """
    Place the colorbar in its new place.

    Parameters
    ----------
    cbax : Axes
        Axes for the colorbar

    renderer :
    w_pad, h_pad : float
        width and height padding (in fraction of figure)
    hspace, wspace : float
        width and height padding as fraction of figure size divided by
        number of  columns or rows
    margin : array-like
        offset the colorbar needs to be pushed to in order to
        account for multiple colorbars
    """

    parents = cbax._colorbar_info['parents']
    gs = parents[0].get_gridspec()
    ncols, nrows = gs.ncols, gs.nrows
    fig = cbax.figure
    trans_fig_to_subfig = fig.transFigure - fig.transSubfigure

    cb_rspans, cb_cspans = _get_cb_parent_spans(cbax)
    bboxparent = gs._layoutgrid.get_bbox_for_cb(rows=cb_rspans, cols=cb_cspans)
    pb = gs._layoutgrid.get_inner_bbox(rows=cb_rspans, cols=cb_cspans)

    location = cbax._colorbar_info['location']
    anchor = cbax._colorbar_info['anchor']
    fraction = cbax._colorbar_info['fraction']
    aspect = cbax._colorbar_info['aspect']
    shrink = cbax._colorbar_info['shrink']

    cbpos, cbbbox = _get_pos_and_bbox(cbax, renderer)

    # Colorbar gets put at extreme edge of outer bbox of the subplotspec
    # It needs to be moved in by: 1) a pad 2) its "margin" 3) by
    # any colorbars already added at this location:
    cbpad = _colorbar_get_pad(cbax)
    if location in ('left', 'right'):
        # fraction and shrink are fractions of parent
        pbcb = pb.shrunk(fraction, shrink).anchored(anchor, pb)
        # The colorbar is at the left side of the parent.  Need
        # to translate to right (or left)
        if location == 'right':
            lmargin = cbpos.x0 - cbbbox.x0
            dx = bboxparent.x1 - pbcb.x0 + offset['right']
            dx += cbpad + lmargin
            offset['right'] += cbbbox.width + cbpad
            pbcb = pbcb.translated(dx, 0)
        else:
            lmargin = cbpos.x0 - cbbbox.x0
            dx = bboxparent.x0 - pbcb.x0  # edge of parent
            dx += -cbbbox.width - cbpad + lmargin - offset['left']
            offset['left'] += cbbbox.width + cbpad
            pbcb = pbcb.translated(dx, 0)
    else:  # horizontal axes:
        pbcb = pb.shrunk(shrink, fraction).anchored(anchor, pb)
        if location == 'top':
            bmargin = cbpos.y0 - cbbbox.y0
            dy = bboxparent.y1 - pbcb.y0 + offset['top']
            dy += cbpad + bmargin
            offset['top'] += cbbbox.height + cbpad
            pbcb = pbcb.translated(0, dy)
        else:
            bmargin = cbpos.y0 - cbbbox.y0
            dy = bboxparent.y0 - pbcb.y0
            dy += -cbbbox.height - cbpad + bmargin - offset['bottom']
            offset['bottom'] += cbbbox.height + cbpad
            pbcb = pbcb.translated(0, dy)

    pbcb = trans_fig_to_subfig.transform_bbox(pbcb)
    cbax.set_transform(fig.transSubfigure)
    cbax._set_position(pbcb)
    cbax.set_aspect(aspect, anchor=anchor, adjustable='box')
    return offset
