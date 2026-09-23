@_api.deprecated("3.4", alternative="Colorbar")
def colorbar_factory(cax, mappable, **kwargs):
    """
    Create a colorbar on the given axes for the given mappable.

    .. note::
        This is a low-level function to turn an existing axes into a colorbar
        axes.  Typically, you'll want to use `~.Figure.colorbar` instead, which
        automatically handles creation and placement of a suitable axes as
        well.

    Parameters
    ----------
    cax : `~matplotlib.axes.Axes`
        The `~.axes.Axes` to turn into a colorbar.
    mappable : `~matplotlib.cm.ScalarMappable`
        The mappable to be described by the colorbar.
    **kwargs
        Keyword arguments are passed to the respective colorbar class.

    Returns
    -------
    `.Colorbar`
        The created colorbar instance.
    """
    return Colorbar(cax, mappable, **kwargs)
