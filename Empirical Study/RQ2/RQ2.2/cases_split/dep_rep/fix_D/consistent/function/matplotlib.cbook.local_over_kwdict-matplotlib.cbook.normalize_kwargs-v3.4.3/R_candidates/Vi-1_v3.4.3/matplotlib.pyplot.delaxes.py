def delaxes(ax=None):
    """
    Remove an `~.axes.Axes` (defaulting to the current axes) from its figure.
    """
    if ax is None:
        ax = gca()
    ax.remove()
