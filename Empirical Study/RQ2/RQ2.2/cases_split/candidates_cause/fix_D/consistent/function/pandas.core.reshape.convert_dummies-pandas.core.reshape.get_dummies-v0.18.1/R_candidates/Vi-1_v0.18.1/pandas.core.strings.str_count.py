def str_count(arr, pat, flags=0):
    """
    Count occurrences of pattern in each string of the Series/Index.

    Parameters
    ----------
    pat : string, valid regular expression
    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE

    Returns
    -------
    counts : Series/Index of integer values
    """
    regex = re.compile(pat, flags=flags)
    f = lambda x: len(regex.findall(x))
    return _na_map(f, arr, dtype=int)
