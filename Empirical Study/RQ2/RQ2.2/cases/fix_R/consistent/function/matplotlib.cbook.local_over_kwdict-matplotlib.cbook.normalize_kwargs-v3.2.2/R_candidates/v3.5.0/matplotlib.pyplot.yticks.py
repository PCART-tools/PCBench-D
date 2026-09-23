def yticks(ticks=None, labels=None, **kwargs):
    """
    Get or set the current tick locations and labels of the y-axis.

    Pass no arguments to return the current values without modifying them.

    Parameters
    ----------
    ticks : array-like, optional
        The list of ytick locations.  Passing an empty list removes all yticks.
    labels : array-like, optional
        The labels to place at the given *ticks* locations.  This argument can
        only be passed if *ticks* is passed as well.
    **kwargs
        `.Text` properties can be used to control the appearance of the labels.

    Returns
    -------
    locs
        The list of ytick locations.
    labels
        The list of ylabel `.Text` objects.

    Notes
    -----
    Calling this function with no arguments (e.g. ``yticks()``) is the pyplot
    equivalent of calling `~.Axes.get_yticks` and `~.Axes.get_yticklabels` on
    the current axes.
    Calling this function with arguments is the pyplot equivalent of calling
    `~.Axes.set_yticks` and `~.Axes.set_yticklabels` on the current axes.

    Examples
    --------
    >>> locs, labels = yticks()  # Get the current locations and labels.
    >>> yticks(np.arange(0, 1, step=0.2))  # Set label locations.
    >>> yticks(np.arange(3), ['Tom', 'Dick', 'Sue'])  # Set text labels.
    >>> yticks([0, 1, 2], ['January', 'February', 'March'],
    ...        rotation=45)  # Set text labels and properties.
    >>> yticks([])  # Disable yticks.
    """
    ax = gca()

    if ticks is None:
        locs = ax.get_yticks()
        if labels is not None:
            raise TypeError("yticks(): Parameter 'labels' can't be set "
                            "without setting 'ticks'")
    else:
        locs = ax.set_yticks(ticks)

    if labels is None:
        labels = ax.get_yticklabels()
        for l in labels:
            l.update(kwargs)
    else:
        labels = ax.set_yticklabels(labels, **kwargs)

    return locs, labels
