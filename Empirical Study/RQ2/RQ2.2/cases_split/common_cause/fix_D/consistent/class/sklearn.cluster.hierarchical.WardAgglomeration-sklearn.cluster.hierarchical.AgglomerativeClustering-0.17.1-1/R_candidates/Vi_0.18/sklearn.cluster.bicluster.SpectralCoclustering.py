class SpectralCoclustering(BaseSpectral):
    """Spectral Co-Clustering algorithm (Dhillon, 2001).

    Clusters rows and columns of an array `X` to solve the relaxed
    normalized cut of the bipartite graph created from `X` as follows:
    the edge between row vertex `i` and column vertex `j` has weight
    `X[i, j]`.

    The resulting bicluster structure is block-diagonal, since each
    row and each column belongs to exactly one bicluster.

    Supports sparse matrices, as long as they are nonnegative.

    Read more in the :ref:`User Guide <spectral_coclustering>`.

    Parameters
    ----------
    n_clusters : integer, optional, default: 3
        The number of biclusters to find.

    svd_method : string, optional, default: 'randomized'
        Selects the algorithm for finding singular vectors. May be
        'randomized' or 'arpack'. If 'randomized', use
        :func:`sklearn.utils.extmath.randomized_svd`, which may be faster
        for large matrices. If 'arpack', use
        :func:`sklearn.utils.arpack.svds`, which is more accurate, but
        possibly slower in some cases.

    n_svd_vecs : int, optional, default: None
        Number of vectors to use in calculating the SVD. Corresponds
        to `ncv` when `svd_method=arpack` and `n_oversamples` when
        `svd_method` is 'randomized`.

    mini_batch : bool, optional, default: False
        Whether to use mini-batch k-means, which is faster but may get
        different results.

    init : {'k-means++', 'random' or an ndarray}
         Method for initialization of k-means algorithm; defaults to
         'k-means++'.

    n_init : int, optional, default: 10
        Number of random initializations that are tried with the
        k-means algorithm.

        If mini-batch k-means is used, the best initialization is
        chosen and the algorithm runs once. Otherwise, the algorithm
        is run for each initialization and the best solution chosen.

    n_jobs : int, optional, default: 1
        The number of jobs to use for the computation. This works by breaking
        down the pairwise matrix into n_jobs even slices and computing them in
        parallel.

        If -1 all CPUs are used. If 1 is given, no parallel computing code is
        used at all, which is useful for debugging. For n_jobs below -1,
        (n_cpus + 1 + n_jobs) are used. Thus for n_jobs = -2, all CPUs but one
        are used.

    random_state : int seed, RandomState instance, or None (default)
        A pseudo random number generator used by the K-Means
        initialization.

    Attributes
    ----------
    rows_ : array-like, shape (n_row_clusters, n_rows)
        Results of the clustering. `rows[i, r]` is True if
        cluster `i` contains row `r`. Available only after calling ``fit``.

    columns_ : array-like, shape (n_column_clusters, n_columns)
        Results of the clustering, like `rows`.

    row_labels_ : array-like, shape (n_rows,)
        The bicluster label of each row.

    column_labels_ : array-like, shape (n_cols,)
        The bicluster label of each column.

    References
    ----------

    * Dhillon, Inderjit S, 2001. `Co-clustering documents and words using
      bipartite spectral graph partitioning
      <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.140.3011>`__.

    """
    def __init__(self, n_clusters=3, svd_method='randomized',
                 n_svd_vecs=None, mini_batch=False, init='k-means++',
                 n_init=10, n_jobs=1, random_state=None):
        super(SpectralCoclustering, self).__init__(n_clusters,
                                                   svd_method,
                                                   n_svd_vecs,
                                                   mini_batch,
                                                   init,
                                                   n_init,
                                                   n_jobs,
                                                   random_state)

    def _fit(self, X):
        normalized_data, row_diag, col_diag = _scale_normalize(X)
        n_sv = 1 + int(np.ceil(np.log2(self.n_clusters)))
        u, v = self._svd(normalized_data, n_sv, n_discard=1)
        z = np.vstack((row_diag[:, np.newaxis] * u,
                       col_diag[:, np.newaxis] * v))

        _, labels = self._k_means(z, self.n_clusters)

        n_rows = X.shape[0]
        self.row_labels_ = labels[:n_rows]
        self.column_labels_ = labels[n_rows:]

        self.rows_ = np.vstack(self.row_labels_ == c
                               for c in range(self.n_clusters))
        self.columns_ = np.vstack(self.column_labels_ == c
                                  for c in range(self.n_clusters))
