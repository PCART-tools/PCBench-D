def right_d_threshold_sequence(n, m):
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

    # connected case m >n-1
    ind = n - 1
    sum = n - 1
    while sum < m:
        cs[ind] = "d"
        ind -= 1
        sum += ind
    ind = m - (sum - ind)
    cs[ind] = "d"
    return cs
