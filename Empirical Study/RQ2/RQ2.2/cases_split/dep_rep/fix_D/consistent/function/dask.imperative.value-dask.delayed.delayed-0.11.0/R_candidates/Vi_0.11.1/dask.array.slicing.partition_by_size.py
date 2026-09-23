def partition_by_size(sizes, seq):
    """

    >>> partition_by_size([10, 20, 10], [1, 5, 9, 12, 29, 35])
    [[1, 5, 9], [2, 19], [5]]
    """
    seq = np.array(seq)
    right = np.cumsum(sizes)
    locations = np.searchsorted(seq, right)
    locations = [0] + locations.tolist()
    left = [0] + right.tolist()
    return [(seq[locations[i]:locations[i + 1]] - left[i]).tolist()
            for i in range(len(locations) - 1)]
