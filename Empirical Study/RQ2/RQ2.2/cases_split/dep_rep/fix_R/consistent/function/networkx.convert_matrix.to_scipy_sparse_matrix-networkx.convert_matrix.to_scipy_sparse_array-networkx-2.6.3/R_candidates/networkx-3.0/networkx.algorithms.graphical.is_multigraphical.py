def is_multigraphical(sequence):
    """Returns True if some multigraph can realize the sequence.

    Parameters
    ----------
    sequence : list
        A list of integers

    Returns
    -------
    valid : bool
        True if deg_sequence is a multigraphic degree sequence and False if not.

    Notes
    -----
    The worst-case run time is $O(n)$ where $n$ is the length of the sequence.

    References
    ----------
    .. [1] S. L. Hakimi. "On the realizability of a set of integers as
       degrees of the vertices of a linear graph", J. SIAM, 10, pp. 496-506
       (1962).
    """
    try:
        deg_sequence = nx.utils.make_list_of_ints(sequence)
    except nx.NetworkXError:
        return False
    dsum, dmax = 0, 0
    for d in deg_sequence:
        if d < 0:
            return False
        dsum, dmax = dsum + d, max(dmax, d)
    if dsum % 2 or dsum < 2 * dmax:
        return False
    return True
