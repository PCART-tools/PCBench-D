def matshow(A, fignum=None, **kwargs):
    """
    Display an array as a matrix in a new figure window.

    The origin is set at the upper left hand corner and rows (first
    dimension of the array) are displayed horizontally.  The aspect
    ratio of the figure window is that of the array, unless this would
    make an excessively short or narrow figure.

    Tick labels for the xaxis are placed on top.

    Parameters
    ----------
    A : 2D array-like
        The matrix to be displayed.

    fignum : None or int or False
        If *None*, create a new figure window with automatic numbering.

        If a nonzero integer, draw into the figure with the given number
        (create it if it does not exist).

        If 0, use the current axes (or create one if it does not exist).

        .. note::

           Because of how `.Axes.matshow` tries to set the figure aspect
           ratio to be the one of the array, strange things may happen if you
           reuse an existing figure.

    Returns
    -------
    `~matplotlib.image.AxesImage`

    Other Parameters
    ----------------
    **kwargs : `~matplotlib.axes.Axes.imshow` arguments

    """
    A = np.asanyarray(A)
    if fignum == 0:
        ax = gca()
    else:
        # Extract actual aspect ratio of array and make appropriately sized
        # figure.
        fig = figure(fignum, figsize=figaspect(A))
        ax = fig.add_axes([0.15, 0.09, 0.775, 0.775])
    im = ax.matshow(A, **kwargs)
    sci(im)
    return im
