def sca(ax):
    """
    Set the current Axes to *ax* and the current Figure to the parent of *ax*.
    """
    figure(ax.figure)
    ax.figure.sca(ax)
