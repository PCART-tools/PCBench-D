def do_constrained_layout(fig, renderer, h_pad, w_pad,
                          hspace=None, wspace=None):
    """
    Do the constrained_layout.  Called at draw time in
     ``figure.constrained_layout()``

    Parameters
    ----------
    fig : Figure
        ``Figure`` instance to do the layout in.

    renderer : Renderer
        Renderer to use.

    h_pad, w_pad : float
      Padding around the axes elements in figure-normalized units.

    hspace, wspace : float
       Fraction of the figure to dedicate to space between the
       axes.  These are evenly spread between the gaps between the axes.
       A value of 0.2 for a three-column layout would have a space
       of 0.1 of the figure width between each column.
       If h/wspace < h/w_pad, then the pads are used instead.

    Returns
    -------
    layoutgrid : private debugging structure
    """

    # make layoutgrid tree...
    layoutgrids = make_layoutgrids(fig, None)
    if not layoutgrids['hasgrids']:
        _api.warn_external('There are no gridspecs with layoutgrids. '
                           'Possibly did not call parent GridSpec with the'
                           ' "figure" keyword')
        return

    for _ in range(2):
        # do the algorithm twice.  This has to be done because decorations
        # change size after the first re-position (i.e. x/yticklabels get
        # larger/smaller).  This second reposition tends to be much milder,
        # so doing twice makes things work OK.

        # make margins for all the axes and subfigures in the
        # figure.  Add margins for colorbars...
        make_layout_margins(layoutgrids, fig, renderer, h_pad=h_pad,
                            w_pad=w_pad, hspace=hspace, wspace=wspace)
        make_margin_suptitles(layoutgrids, fig, renderer, h_pad=h_pad,
                              w_pad=w_pad)

        # if a layout is such that a columns (or rows) margin has no
        # constraints, we need to make all such instances in the grid
        # match in margin size.
        match_submerged_margins(layoutgrids, fig)

        # update all the variables in the layout.
        layoutgrids[fig].update_variables()

        if check_no_collapsed_axes(layoutgrids, fig):
            reposition_axes(layoutgrids, fig, renderer, h_pad=h_pad,
                            w_pad=w_pad, hspace=hspace, wspace=wspace)
        else:
            _api.warn_external('constrained_layout not applied because '
                               'axes sizes collapsed to zero.  Try making '
                               'figure larger or axes decorations smaller.')
        reset_margins(layoutgrids, fig)
    return layoutgrids
