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
    """

    # list of unique gridspecs that contain child axes:
    gss = set()
    for ax in fig.axes:
        if hasattr(ax, 'get_subplotspec'):
            gs = ax.get_subplotspec().get_gridspec()
            if gs._layoutgrid is not None:
                gss.add(gs)
    gss = list(gss)
    if len(gss) == 0:
        _api.warn_external('There are no gridspecs with layoutgrids. '
                           'Possibly did not call parent GridSpec with the'
                           ' "figure" keyword')

    for _ in range(2):
        # do the algorithm twice.  This has to be done because decorations
        # change size after the first re-position (i.e. x/yticklabels get
        # larger/smaller).  This second reposition tends to be much milder,
        # so doing twice makes things work OK.

        # make margins for all the axes and subfigures in the
        # figure.  Add margins for colorbars...
        _make_layout_margins(fig, renderer, h_pad=h_pad, w_pad=w_pad,
                             hspace=hspace, wspace=wspace)
        _make_margin_suptitles(fig, renderer, h_pad=h_pad, w_pad=w_pad)

        # if a layout is such that a columns (or rows) margin has no
        # constraints, we need to make all such instances in the grid
        # match in margin size.
        _match_submerged_margins(fig)

        # update all the variables in the layout.
        fig._layoutgrid.update_variables()

        if _check_no_collapsed_axes(fig):
            _reposition_axes(fig, renderer, h_pad=h_pad, w_pad=w_pad,
                             hspace=hspace, wspace=wspace)
        else:
            _api.warn_external('constrained_layout not applied because '
                               'axes sizes collapsed to zero.  Try making '
                               'figure larger or axes decorations smaller.')
        _reset_margins(fig)
