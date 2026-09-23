def str_get_dummies(arr, sep='|'):
    """
    Split each string in the Series by sep and return a frame of
    dummy/indicator variables.

    Parameters
    ----------
    sep : string, default "|"
        String to split on.

    Returns
    -------
    dummies : DataFrame

    Examples
    --------
    >>> Series(['a|b', 'a', 'a|c']).str.get_dummies()
       a  b  c
    0  1  1  0
    1  1  0  0
    2  1  0  1

    >>> Series(['a|b', np.nan, 'a|c']).str.get_dummies()
       a  b  c
    0  1  1  0
    1  0  0  0
    2  1  0  1

    See Also
    --------
    pandas.get_dummies
    """
    arr = arr.fillna('')
    try:
        arr = sep + arr + sep
    except TypeError:
        arr = sep + arr.astype(str) + sep

    tags = set()
    for ts in arr.str.split(sep):
        tags.update(ts)
    tags = sorted(tags - set([""]))

    dummies = np.empty((len(arr), len(tags)), dtype=np.int64)

    for i, t in enumerate(tags):
        pat = sep + t + sep
        dummies[:, i] = lib.map_infer(arr.values, lambda x: pat in x)
    return dummies, tags
