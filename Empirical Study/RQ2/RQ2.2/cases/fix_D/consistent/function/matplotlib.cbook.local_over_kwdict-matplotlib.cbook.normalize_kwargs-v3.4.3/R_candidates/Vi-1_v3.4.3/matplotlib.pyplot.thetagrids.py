def thetagrids(angles=None, labels=None, fmt=None, **kwargs):
    """
    Get or set the theta gridlines on the current polar plot.

    Call signatures::

     lines, labels = thetagrids()
     lines, labels = thetagrids(angles, labels=None, fmt=None, **kwargs)

    When called with no arguments, `.thetagrids` simply returns the tuple
    (*lines*, *labels*). When called with arguments, the labels will
    appear at the specified angles.

    Parameters
    ----------
    angles : tuple with floats, degrees
        The angles of the theta gridlines.

    labels : tuple with strings or None
        The labels to use at each radial gridline. The
        `.projections.polar.ThetaFormatter` will be used if None.

    fmt : str or None
        Format string used in `matplotlib.ticker.FormatStrFormatter`.
        For example '%f'. Note that the angle in radians will be used.

    Returns
    -------
    lines : list of `.lines.Line2D`
        The theta gridlines.

    labels : list of `.text.Text`
        The tick labels.

    Other Parameters
    ----------------
    **kwargs
        *kwargs* are optional `~.Text` properties for the labels.

    See Also
    --------
    .pyplot.rgrids
    .projections.polar.PolarAxes.set_thetagrids
    .Axis.get_gridlines
    .Axis.get_ticklabels

    Examples
    --------
    ::

      # set the locations of the angular gridlines
      lines, labels = thetagrids(range(45, 360, 90))

      # set the locations and labels of the angular gridlines
      lines, labels = thetagrids(range(45, 360, 90), ('NE', 'NW', 'SW', 'SE'))
    """
    ax = gca()
    if not isinstance(ax, PolarAxes):
        raise RuntimeError('thetagrids only defined for polar axes')
    if all(param is None for param in [angles, labels, fmt]) and not kwargs:
        lines = ax.xaxis.get_ticklines()
        labels = ax.xaxis.get_ticklabels()
    else:
        lines, labels = ax.set_thetagrids(angles,
                                          labels=labels, fmt=fmt, **kwargs)
    return lines, labels
