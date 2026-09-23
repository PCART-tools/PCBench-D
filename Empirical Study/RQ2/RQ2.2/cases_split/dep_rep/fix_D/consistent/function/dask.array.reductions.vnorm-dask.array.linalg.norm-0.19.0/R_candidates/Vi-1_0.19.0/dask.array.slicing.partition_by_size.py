def partition_by_size(sizes, seq):
    """

    >>> partition_by_size([10, 20, 10], [1, 5, 9, 12, 29, 35])
    [array([1, 5, 9]), array([ 2, 19]), array([5])]
    """
    seq = np.asanyarray(seq)
    left = np.empty(len(sizes) + 1, dtype=int)
    left[0] = 0

    right = np.cumsum(sizes, out=left[1:])
    locations = np.empty(len(sizes) + 1, dtype=int)
    locations[0] = 0
    locations[1:] = np.searchsorted(seq, right)
    return [(seq[j:k] - l)
            for j, k, l in zip(locations[:-1], locations[1:], left)]
