def count_tied_groups(x, use_missing=False):
    """
    Counts the number of tied values.

    Parameters
    ----------
    x : sequence
        Sequence of data on which to counts the ties
    use_missing : boolean
        Whether to consider missing values as tied.

    Returns
    -------
    count_tied_groups : dict
        Returns a dictionary (nb of ties: nb of groups).

    Examples
    --------
    >>> z = [0, 0, 0, 2, 2, 2, 3, 3, 4, 5, 6]
    >>> count_tied_groups(z)
    >>> {2:1, 3:2}
    >>> # The ties were 0 (3x), 2 (3x) and 3 (2x)
    >>> z = ma.array([0, 0, 1, 2, 2, 2, 3, 3, 4, 5, 6])
    >>> count_tied_groups(z)
    >>> {2:2, 3:1}
    >>> # The ties were 0 (2x), 2 (3x) and 3 (2x)
    >>> z[[1,-1]] = masked
    >>> count_tied_groups(z, use_missing=True)
    >>> {2:2, 3:1}
    >>> # The ties were 2 (3x), 3 (2x) and masked (2x)

    """
    nmasked = ma.getmask(x).sum()
    # We need the copy as find_repeats will overwrite the initial data
    data = ma.compressed(x).copy()
    (ties, counts) = find_repeats(data)
    nties = {}
    if len(ties):
        nties = dict(zip(np.unique(counts), itertools.repeat(1)))
        nties.update(dict(zip(*find_repeats(counts))))
    if nmasked and use_missing:
        try:
            nties[nmasked] += 1
        except KeyError:
            nties[nmasked] = 1
    return nties
