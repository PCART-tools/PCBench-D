def str_contains(arr, pat, case=True, flags=0, na=np.nan, regex=True):
    """
    Return boolean Series/``array`` whether given pattern/regex is
    contained in each string in the Series/Index.

    Parameters
    ----------
    pat : string
        Character sequence or regular expression
    case : boolean, default True
        If True, case sensitive
    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE
    na : default NaN, fill value for missing values.
    regex : bool, default True
        If True use re.search, otherwise use Python in operator

    Returns
    -------
    contained : Series/array of boolean values

    See Also
    --------
    match : analogous, but stricter, relying on re.match instead of re.search

    """
    if regex:
        if not case:
            flags |= re.IGNORECASE

        regex = re.compile(pat, flags=flags)

        if regex.groups > 0:
            warnings.warn("This pattern has match groups. To actually get the"
                          " groups, use str.extract.", UserWarning,
                          stacklevel=3)

        f = lambda x: bool(regex.search(x))
    else:
        if case:
            f = lambda x: pat in x
        else:
            upper_pat = pat.upper()
            f = lambda x: upper_pat in x
            uppered = _na_map(lambda x: x.upper(), arr)
            return _na_map(f, uppered, na, dtype=bool)
    return _na_map(f, arr, na, dtype=bool)
