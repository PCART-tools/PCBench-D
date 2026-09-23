def left_d_threshold_sequence(n, m):
    """
    Create a skewed threshold graph with a given number
    of vertices (n) and a given number of edges (m).

    The routine returns an unlabeled creation sequence
    for the threshold graph.

    FIXME: describe algorithm

    """
    cs = ["d"] + ["i"] * (n - 1)  # create sequence with n insolated nodes

    #  m <n : not enough edges, make disconnected
    if m < n:
        cs[m] = "d"
        return cs

    # too many edges
    if m > n * (n - 1) / 2:
        raise ValueError("Too many edges for this many nodes.")

    # Connected case when M>N-1
    cs[n - 1] = "d"
    sum = n - 1
    ind = 1
    while sum < m:
        cs[ind] = "d"
        sum += ind
        ind += 1
    if sum > m:  # be sure not to change the first vertex
        cs[sum - m] = "i"
    return cs
