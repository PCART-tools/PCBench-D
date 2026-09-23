def str_count(arr, pat, flags=0):
    """
    Count occurrences of pattern in each string

    Parameters
    ----------
    arr : list or array-like
    pat : string, valid regular expression
    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE

    Returns
    -------
    counts : arrays
    """
    regex = re.compile(pat, flags=flags)
    f = lambda x: len(regex.findall(x))
    return _na_map(f, arr, dtype=int)
