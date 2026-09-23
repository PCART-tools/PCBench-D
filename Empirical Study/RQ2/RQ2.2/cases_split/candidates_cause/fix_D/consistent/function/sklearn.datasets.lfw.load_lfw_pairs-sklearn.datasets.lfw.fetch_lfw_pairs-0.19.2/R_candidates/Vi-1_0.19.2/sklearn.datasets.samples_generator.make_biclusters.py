def make_biclusters(shape, n_clusters, noise=0.0, minval=10,
                    maxval=100, shuffle=True, random_state=None):
    """Generate an array with constant block diagonal structure for
    biclustering.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    shape : iterable (n_rows, n_cols)
        The shape of the result.

    n_clusters : integer
        The number of biclusters.

    noise : float, optional (default=0.0)
        The standard deviation of the gaussian noise.

    minval : int, optional (default=10)
        Minimum value of a bicluster.

    maxval : int, optional (default=100)
        Maximum value of a bicluster.

    shuffle : boolean, optional (default=True)
        Shuffle the samples.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    Returns
    -------
    X : array of shape `shape`
        The generated array.

    rows : array of shape (n_clusters, X.shape[0],)
        The indicators for cluster membership of each row.

    cols : array of shape (n_clusters, X.shape[1],)
        The indicators for cluster membership of each column.

    References
    ----------

    .. [1] Dhillon, I. S. (2001, August). Co-clustering documents and
        words using bipartite spectral graph partitioning. In Proceedings
        of the seventh ACM SIGKDD international conference on Knowledge
        discovery and data mining (pp. 269-274). ACM.

    See also
    --------
    make_checkerboard
    """
    generator = check_random_state(random_state)
    n_rows, n_cols = shape
    consts = generator.uniform(minval, maxval, n_clusters)

    # row and column clusters of approximately equal sizes
    row_sizes = generator.multinomial(n_rows,
                                      np.repeat(1.0 / n_clusters,
                                                n_clusters))
    col_sizes = generator.multinomial(n_cols,
                                      np.repeat(1.0 / n_clusters,
                                                n_clusters))

    row_labels = np.hstack(list(np.repeat(val, rep) for val, rep in
                                zip(range(n_clusters), row_sizes)))
    col_labels = np.hstack(list(np.repeat(val, rep) for val, rep in
                                zip(range(n_clusters), col_sizes)))

    result = np.zeros(shape, dtype=np.float64)
    for i in range(n_clusters):
        selector = np.outer(row_labels == i, col_labels == i)
        result[selector] += consts[i]

    if noise > 0:
        result += generator.normal(scale=noise, size=result.shape)

    if shuffle:
        result, row_idx, col_idx = _shuffle(result, random_state)
        row_labels = row_labels[row_idx]
        col_labels = col_labels[col_idx]

    rows = np.vstack(row_labels == c for c in range(n_clusters))
    cols = np.vstack(col_labels == c for c in range(n_clusters))

    return result, rows, cols
