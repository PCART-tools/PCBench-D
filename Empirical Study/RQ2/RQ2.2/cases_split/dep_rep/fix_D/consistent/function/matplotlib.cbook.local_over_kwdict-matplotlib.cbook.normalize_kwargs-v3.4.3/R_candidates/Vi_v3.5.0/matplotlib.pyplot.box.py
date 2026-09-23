def box(on=None):
    """
    Turn the axes box on or off on the current axes.

    Parameters
    ----------
    on : bool or None
        The new `~matplotlib.axes.Axes` box state. If ``None``, toggle
        the state.

    See Also
    --------
    :meth:`matplotlib.axes.Axes.set_frame_on`
    :meth:`matplotlib.axes.Axes.get_frame_on`
    """
    ax = gca()
    if on is None:
        on = not ax.get_frame_on()
    ax.set_frame_on(on)
