def str_extract(arr, pat, flags=0, expand=None):
    """
    For each subject string in the Series, extract groups from the
    first match of regular expression pat.

    .. versionadded:: 0.13.0

    Parameters
    ----------
    pat : string
        Regular expression pattern with capturing groups
    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE

    .. versionadded:: 0.18.0
    expand : bool, default False
        * If True, return DataFrame.
        * If False, return Series/Index/DataFrame.

    Returns
    -------
    DataFrame with one row for each subject string, and one column for
    each group. Any capture group names in regular expression pat will
    be used for column names; otherwise capture group numbers will be
    used. The dtype of each result column is always object, even when
    no match is found. If expand=False and pat has only one capture group,
    then return a Series (if subject is a Series) or Index (if subject
    is an Index).

    See Also
    --------
    extractall : returns all matches (not just the first match)

    Examples
    --------
    A pattern with two groups will return a DataFrame with two columns.
    Non-matches will be NaN.

    >>> s = Series(['a1', 'b2', 'c3'])
    >>> s.str.extract('([ab])(\d)')
         0    1
    0    a    1
    1    b    2
    2  NaN  NaN

    A pattern may contain optional groups.

    >>> s.str.extract('([ab])?(\d)')
         0  1
    0    a  1
    1    b  2
    2  NaN  3

    Named groups will become column names in the result.

    >>> s.str.extract('(?P<letter>[ab])(?P<digit>\d)')
      letter digit
    0      a     1
    1      b     2
    2    NaN   NaN

    A pattern with one group will return a DataFrame with one column
    if expand=True.

    >>> s.str.extract('[ab](\d)', expand=True)
         0
    0    1
    1    2
    2  NaN

    A pattern with one group will return a Series if expand=False.

    >>> s.str.extract('[ab](\d)', expand=False)
    0      1
    1      2
    2    NaN
    dtype: object

    """
    if expand is None:
        warnings.warn(
            "currently extract(expand=None) " +
            "means expand=False (return Index/Series/DataFrame) " +
            "but in a future version of pandas this will be changed " +
            "to expand=True (return DataFrame)",
            FutureWarning,
            stacklevel=3)
        expand = False
    if not isinstance(expand, bool):
        raise ValueError("expand must be True or False")
    if expand:
        return _str_extract_frame(arr._orig, pat, flags=flags)
    else:
        result, name = _str_extract_noexpand(arr._data, pat, flags=flags)
        return arr._wrap_result(result, name=name, expand=expand)
