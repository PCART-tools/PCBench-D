def str_match(arr, pat, case=True, flags=0, na=np.nan, as_indexer=False):
    """
    Deprecated: Find groups in each string in the Series/Index
    using passed regular expression.
    If as_indexer=True, determine if each string matches a regular expression.

    Parameters
    ----------
    pat : string
        Character sequence or regular expression
    case : boolean, default True
        If True, case sensitive
    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE
    na : default NaN, fill value for missing values.
    as_indexer : False, by default, gives deprecated behavior better achieved
        using str_extract. True return boolean indexer.

    Returns
    -------
    Series/array of boolean values
        if as_indexer=True
    Series/Index of tuples
        if as_indexer=False, default but deprecated

    See Also
    --------
    contains : analogous, but less strict, relying on re.search instead of
        re.match
    extract : now preferred to the deprecated usage of match (as_indexer=False)

    Notes
    -----
    To extract matched groups, which is the deprecated behavior of match, use
    str.extract.
    """

    if not case:
        flags |= re.IGNORECASE

    regex = re.compile(pat, flags=flags)

    if (not as_indexer) and regex.groups > 0:
        # Do this first, to make sure it happens even if the re.compile
        # raises below.
        warnings.warn("In future versions of pandas, match will change to"
                      " always return a bool indexer.", FutureWarning,
                      stacklevel=3)

    if as_indexer and regex.groups > 0:
        warnings.warn("This pattern has match groups. To actually get the"
                      " groups, use str.extract.", UserWarning, stacklevel=3)

    # If not as_indexer and regex.groups == 0, this returns empty lists
    # and is basically useless, so we will not warn.

    if (not as_indexer) and regex.groups > 0:
        dtype = object

        def f(x):
            m = regex.match(x)
            if m:
                return m.groups()
            else:
                return []
    else:
        # This is the new behavior of str_match.
        dtype = bool
        f = lambda x: bool(regex.match(x))

    return _na_map(f, arr, na, dtype=dtype)
