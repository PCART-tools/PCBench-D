def pivot_simple(index, columns, values):
    """
    Produce 'pivot' table based on 3 columns of this DataFrame.
    Uses unique values from index / columns and fills with values.

    Parameters
    ----------
    index : ndarray
        Labels to use to make new frame's index
    columns : ndarray
        Labels to use to make new frame's columns
    values : ndarray
        Values to use for populating new frame's values

    Notes
    -----
    Obviously, all 3 of the input arguments must have the same length

    Returns
    -------
    DataFrame
    """
    if (len(index) != len(columns)) or (len(columns) != len(values)):
        raise AssertionError('Length of index, columns, and values must be the'
                             ' same')

    if len(index) == 0:
        return DataFrame(index=[])

    hindex = MultiIndex.from_arrays([index, columns])
    series = Series(values.ravel(), index=hindex)
    series = series.sortlevel(0)
    return series.unstack()
