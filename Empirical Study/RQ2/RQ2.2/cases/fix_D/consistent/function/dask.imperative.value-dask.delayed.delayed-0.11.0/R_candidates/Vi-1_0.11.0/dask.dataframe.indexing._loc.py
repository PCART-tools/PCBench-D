def _loc(df, start, stop, include_right_boundary=True):
    """

    >>> df = pd.DataFrame({'x': [10, 20, 30, 40, 50]}, index=[1, 2, 2, 3, 4])
    >>> _loc(df, 2, None)
        x
    2  20
    2  30
    3  40
    4  50
    >>> _loc(df, 1, 3)
        x
    1  10
    2  20
    2  30
    3  40
    >>> _loc(df, 1, 3, include_right_boundary=False)
        x
    1  10
    2  20
    2  30
    """
    result = df.loc[start:stop]
    if not include_right_boundary:
        right_index = result.index.get_slice_bound(stop, 'left', 'loc')
        result = result.iloc[:right_index]
    return result
