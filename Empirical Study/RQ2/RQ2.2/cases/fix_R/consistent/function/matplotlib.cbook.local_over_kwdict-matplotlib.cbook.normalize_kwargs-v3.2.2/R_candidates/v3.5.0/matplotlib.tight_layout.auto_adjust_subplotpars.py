@_api.deprecated("3.5")
def auto_adjust_subplotpars(
        fig, renderer, nrows_ncols, num1num2_list, subplot_list,
        ax_bbox_list=None, pad=1.08, h_pad=None, w_pad=None, rect=None):
    """
    Return a dict of subplot parameters to adjust spacing between subplots
    or ``None`` if resulting axes would have zero height or width.

    Note that this function ignores geometry information of subplot
    itself, but uses what is given by the *nrows_ncols* and *num1num2_list*
    parameters.  Also, the results could be incorrect if some subplots have
    ``adjustable=datalim``.

    Parameters
    ----------
    nrows_ncols : tuple[int, int]
        Number of rows and number of columns of the grid.
    num1num2_list : list[tuple[int, int]]
        List of numbers specifying the area occupied by the subplot
    subplot_list : list of subplots
        List of subplots that will be used to calculate optimal subplot_params.
    pad : float
        Padding between the figure edge and the edges of subplots, as a
        fraction of the font size.
    h_pad, w_pad : float
        Padding (height/width) between edges of adjacent subplots, as a
        fraction of the font size.  Defaults to *pad*.
    rect : tuple[float, float, float, float]
        [left, bottom, right, top] in normalized (0, 1) figure coordinates.
    """
    nrows, ncols = nrows_ncols
    span_pairs = []
    for n1, n2 in num1num2_list:
        if n2 is None:
            n2 = n1
        span_pairs.append((slice(n1 // ncols, n2 // ncols + 1),
                           slice(n1 % ncols, n2 % ncols + 1)))
    return _auto_adjust_subplotpars(
        fig, renderer, nrows_ncols, num1num2_list, subplot_list,
        ax_bbox_list, pad, h_pad, w_pad, rect)
