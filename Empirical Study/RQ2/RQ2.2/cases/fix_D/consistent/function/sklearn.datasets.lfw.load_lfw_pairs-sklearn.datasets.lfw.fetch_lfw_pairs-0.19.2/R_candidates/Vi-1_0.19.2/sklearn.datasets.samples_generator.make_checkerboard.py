def make_checkerboard(shape, n_clusters, noise=0.0, minval=10,
                      maxval=100, shuffle=True, random_state=None):

    """Generate an array with block checkerboard structure for
    biclustering.

    Read more in the :ref:`User Guide <sample_generators>`.

    Parameters
    ----------
    shape : iterable (n_rows, n_cols)
        The shape of the result.

    n_clusters : integer or iterable (n_row_clusters, n_column_clusters)
        The number of row and column clusters.

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

    .. [1] Kluger, Y., Basri, R., Chang, J. T., & Gerstein, M. (2003).
        Spectral biclustering of microarray data: coclustering genes
        and conditions. Genome research, 13(4), 703-716.

    See also
    --------
    make_biclusters
    """
    generator = check_random_state(random_state)

    if hasattr(n_clusters, "__len__"):
        n_row_clusters, n_col_clusters = n_clusters
    else:
        n_row_clusters = n_col_clusters = n_clusters

    # row and column clusters of approximately equal sizes
    n_rows, n_cols = shape
    row_sizes = generator.multinomial(n_rows,
                                      np.repeat(1.0 / n_row_clusters,
                                                n_row_clusters))
    col_sizes = generator.multinomial(n_cols,
                                      np.repeat(1.0 / n_col_clusters,
                                                n_col_clusters))

    row_labels = np.hstack(list(np.repeat(val, rep) for val, rep in
                                zip(range(n_row_clusters), row_sizes)))
    col_labels = np.hstack(list(np.repeat(val, rep) for val, rep in
                                zip(range(n_col_clusters), col_sizes)))

    result = np.zeros(shape, dtype=np.float64)
    for i in range(n_row_clusters):
        for j in range(n_col_clusters):
            selector = np.outer(row_labels == i, col_labels == j)
            result[selector] += generator.uniform(minval, maxval)

    if noise > 0:
        result += generator.normal(scale=noise, size=result.shape)

    if shuffle:
        result, row_idx, col_idx = _shuffle(result, random_state)
        row_labels = row_labels[row_idx]
        col_labels = col_labels[col_idx]

    rows = np.vstack(row_labels == label
                     for label in range(n_row_clusters)
                     for _ in range(n_col_clusters))
    cols = np.vstack(col_labels == label
                     for _ in range(n_row_clusters)
                     for label in range(n_col_clusters))

    return result, rows, cols
