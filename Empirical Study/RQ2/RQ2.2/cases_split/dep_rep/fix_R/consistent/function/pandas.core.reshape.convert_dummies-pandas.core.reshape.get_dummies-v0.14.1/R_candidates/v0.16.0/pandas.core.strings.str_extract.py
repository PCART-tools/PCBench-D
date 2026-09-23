def str_extract(arr, pat, flags=0):
    """
    Find groups in each string using passed regular expression

    Parameters
    ----------
    pat : string
        Pattern or regular expression
    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE

    Returns
    -------
    extracted groups : Series (one group) or DataFrame (multiple groups)
        Note that dtype of the result is always object, even when no match is
        found and the result is a Series or DataFrame containing only NaN
        values.

    Examples
    --------
    A pattern with one group will return a Series. Non-matches will be NaN.

    >>> Series(['a1', 'b2', 'c3']).str.extract('[ab](\d)')
    0      1
    1      2
    2    NaN
    dtype: object

    A pattern with more than one group will return a DataFrame.

    >>> Series(['a1', 'b2', 'c3']).str.extract('([ab])(\d)')
         0    1
    0    a    1
    1    b    2
    2  NaN  NaN

    A pattern may contain optional groups.

    >>> Series(['a1', 'b2', 'c3']).str.extract('([ab])?(\d)')
         0  1
    0    a  1
    1    b  2
    2  NaN  3

    Named groups will become column names in the result.

    >>> Series(['a1', 'b2', 'c3']).str.extract('(?P<letter>[ab])(?P<digit>\d)')
      letter digit
    0      a     1
    1      b     2
    2    NaN   NaN

    """
    from pandas.core.series import Series
    from pandas.core.frame import DataFrame

    regex = re.compile(pat, flags=flags)
    # just to be safe, check this
    if regex.groups == 0:
        raise ValueError("This pattern contains no groups to capture.")
    empty_row = [np.nan]*regex.groups
    def f(x):
        if not isinstance(x, compat.string_types):
            return empty_row
        m = regex.search(x)
        if m:
            return [np.nan if item is None else item for item in m.groups()]
        else:
            return empty_row
    if regex.groups == 1:
        result = Series([f(val)[0] for val in arr],
                        name=_get_single_group_name(regex),
                        index=arr.index, dtype=object)
    else:
        names = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
        columns = [names.get(1 + i, i) for i in range(regex.groups)]
        if arr.empty:
            result = DataFrame(columns=columns, dtype=object)
        else:
            result = DataFrame([f(val) for val in arr],
                               columns=columns,
                               index=arr.index,
                               dtype=object)
    return result
