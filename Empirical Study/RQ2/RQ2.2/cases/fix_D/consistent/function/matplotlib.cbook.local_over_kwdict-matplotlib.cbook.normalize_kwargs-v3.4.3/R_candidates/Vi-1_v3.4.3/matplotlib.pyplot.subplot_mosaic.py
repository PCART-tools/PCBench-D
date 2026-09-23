def subplot_mosaic(mosaic, *, subplot_kw=None, gridspec_kw=None,
                   empty_sentinel='.', **fig_kw):
    """
    Build a layout of Axes based on ASCII art or nested lists.

    This is a helper function to build complex GridSpec layouts visually.

    .. note ::

       This API is provisional and may be revised in the future based on
       early user feedback.


    Parameters
    ----------
    mosaic : list of list of {hashable or nested} or str

        A visual layout of how you want your Axes to be arranged
        labeled as strings.  For example ::

           x = [['A panel', 'A panel', 'edge'],
                ['C panel', '.',       'edge']]

        Produces 4 axes:

        - 'A panel' which is 1 row high and spans the first two columns
        - 'edge' which is 2 rows high and is on the right edge
        - 'C panel' which in 1 row and 1 column wide in the bottom left
        - a blank space 1 row and 1 column wide in the bottom center

        Any of the entries in the layout can be a list of lists
        of the same form to create nested layouts.

        If input is a str, then it must be of the form ::

          '''
          AAE
          C.E
          '''

        where each character is a column and each line is a row.
        This only allows only single character Axes labels and does
        not allow nesting but is very terse.

    subplot_kw : dict, optional
        Dictionary with keywords passed to the `.Figure.add_subplot` call
        used to create each subplot.

    gridspec_kw : dict, optional
        Dictionary with keywords passed to the `.GridSpec` constructor used
        to create the grid the subplots are placed on.

    empty_sentinel : object, optional
        Entry in the layout to mean "leave this space empty".  Defaults
        to ``'.'``. Note, if *layout* is a string, it is processed via
        `inspect.cleandoc` to remove leading white space, which may
        interfere with using white-space as the empty sentinel.

    **fig_kw
        All additional keyword arguments are passed to the
        `.pyplot.figure` call.

    Returns
    -------
    fig : `~.figure.Figure`
       The new figure

    dict[label, Axes]
       A dictionary mapping the labels to the Axes objects.  The order of
       the axes is left-to-right and top-to-bottom of their position in the
       total layout.

    """
    fig = figure(**fig_kw)
    ax_dict = fig.subplot_mosaic(
        mosaic,
        subplot_kw=subplot_kw,
        gridspec_kw=gridspec_kw,
        empty_sentinel=empty_sentinel
    )
    return fig, ax_dict
