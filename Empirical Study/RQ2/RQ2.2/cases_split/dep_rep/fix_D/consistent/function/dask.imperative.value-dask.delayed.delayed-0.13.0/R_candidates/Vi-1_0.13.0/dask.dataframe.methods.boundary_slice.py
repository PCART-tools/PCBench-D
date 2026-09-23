def boundary_slice(df, start, stop, right_boundary=True, left_boundary=True,
                   kind='loc'):
    """Index slice start/stop. Can switch include/exclude boundaries.

    >>> df = pd.DataFrame({'x': [10, 20, 30, 40, 50]}, index=[1, 2, 2, 3, 4])
    >>> boundary_slice(df, 2, None)
        x
    2  20
    2  30
    3  40
    4  50
    >>> boundary_slice(df, 1, 3)
        x
    1  10
    2  20
    2  30
    3  40
    >>> boundary_slice(df, 1, 3, right_boundary=False)
        x
    1  10
    2  20
    2  30
    """
    result = getattr(df, kind)[start:stop]
    if not right_boundary:
        right_index = result.index.get_slice_bound(stop, 'left', kind)
        result = result.iloc[:right_index]
    if not left_boundary:
        left_index = result.index.get_slice_bound(start, 'right', kind)
        result = result.iloc[left_index:]
    return result
