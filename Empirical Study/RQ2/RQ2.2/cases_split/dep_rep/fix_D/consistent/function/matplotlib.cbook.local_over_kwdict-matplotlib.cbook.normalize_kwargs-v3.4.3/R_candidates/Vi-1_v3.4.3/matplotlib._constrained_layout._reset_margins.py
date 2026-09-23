def _reset_margins(fig):
    """
    Reset the margins in the layoutboxes of fig.

    Margins are usually set as a minimum, so if the figure gets smaller
    the minimum needs to be zero in order for it to grow again.
    """
    for span in fig.subfigs:
        _reset_margins(span)
    for ax in fig.axes:
        if hasattr(ax, 'get_subplotspec') and ax.get_in_layout():
            ss = ax.get_subplotspec()
            gs = ss.get_gridspec()
            if gs._layoutgrid is not None:
                gs._layoutgrid.reset_margins()
    fig._layoutgrid.reset_margins()
