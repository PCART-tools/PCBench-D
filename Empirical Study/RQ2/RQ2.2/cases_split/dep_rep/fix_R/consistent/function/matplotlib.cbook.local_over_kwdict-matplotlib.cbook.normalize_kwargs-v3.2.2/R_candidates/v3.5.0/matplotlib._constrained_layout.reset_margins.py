def reset_margins(layoutgrids, fig):
    """
    Reset the margins in the layoutboxes of fig.

    Margins are usually set as a minimum, so if the figure gets smaller
    the minimum needs to be zero in order for it to grow again.
    """
    for sfig in fig.subfigs:
        reset_margins(layoutgrids, sfig)
    for ax in fig.axes:
        if hasattr(ax, 'get_subplotspec') and ax.get_in_layout():
            ss = ax.get_subplotspec()
            gs = ss.get_gridspec()
            if gs in layoutgrids:
                layoutgrids[gs].reset_margins()
    layoutgrids[fig].reset_margins()
