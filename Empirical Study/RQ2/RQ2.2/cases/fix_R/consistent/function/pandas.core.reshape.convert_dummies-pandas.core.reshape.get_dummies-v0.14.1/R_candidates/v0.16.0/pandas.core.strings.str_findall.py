def str_findall(arr, pat, flags=0):
    """
    Find all occurrences of pattern or regular expression

    Parameters
    ----------
    pat : string
        Pattern or regular expression
    flags : int, default 0 (no flags)
        re module flags, e.g. re.IGNORECASE

    Returns
    -------
    matches : array
    """
    regex = re.compile(pat, flags=flags)
    return _na_map(regex.findall, arr)
