class SpectralBiclustering(BaseSpectral):
    """Spectral biclustering (Kluger, 2003).

    Partitions rows and columns under the assumption that the data has
    an underlying checkerboard structure. For instance, if there are
    two row partitions and three column partitions, each row will
    belong to three biclusters, and each column will belong to two
    biclusters. The outer product of the corresponding row and column
    label vectors gives this checkerboard structure.

    Read more in the :ref:`User Guide <spectral_biclustering>`.

    Parameters
    ----------
    n_clusters : integer or tuple (n_row_clusters, n_column_clusters)
        The number of row and column clusters in the checkerboard
        structure.

    method : string, optional, default: 'bistochastic'
        Method of normalizing and converting singular vectors into
        biclusters. May be one of 'scale', 'bistochastic', or 'log'.
        The authors recommend using 'log'. If the data is sparse,
        however, log normalization will not work, which is why the
        default is 'bistochastic'. CAUTION: if `method='log'`, the
        data must not be sparse.

    n_components : integer, optional, default: 6
        Number of singular vectors to check.

    n_best : integer, optional, default: 3
        Number of best singular vectors to which to project the data
        for clustering.

    svd_method : string, optional, default: 'randomized'
        Selects the algorithm for finding singular vectors. May be
        'randomized' or 'arpack'. If 'randomized', uses
        `sklearn.utils.extmath.randomized_svd`, which may be faster
        for large matrices. If 'arpack', uses
        `sklearn.utils.arpack.svds`, which is more accurate, but
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
        Row partition labels.

    column_labels_ : array-like, shape (n_cols,)
        Column partition labels.

    References
    ----------

    * Kluger, Yuval, et. al., 2003. `Spectral biclustering of microarray
      data: coclustering genes and conditions
      <http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.135.1608>`__.

    """
    def __init__(self, n_clusters=3, method='bistochastic',
                 n_components=6, n_best=3, svd_method='randomized',
                 n_svd_vecs=None, mini_batch=False, init='k-means++',
                 n_init=10, n_jobs=1, random_state=None):
        super(SpectralBiclustering, self).__init__(n_clusters,
                                                   svd_method,
                                                   n_svd_vecs,
                                                   mini_batch,
                                                   init,
                                                   n_init,
                                                   n_jobs,
                                                   random_state)
        self.method = method
        self.n_components = n_components
        self.n_best = n_best

    def _check_parameters(self):
        super(SpectralBiclustering, self)._check_parameters()
        legal_methods = ('bistochastic', 'scale', 'log')
        if self.method not in legal_methods:
            raise ValueError("Unknown method: '{0}'. method must be"
                             " one of {1}.".format(self.method, legal_methods))
        try:
            int(self.n_clusters)
        except TypeError:
            try:
                r, c = self.n_clusters
                int(r)
                int(c)
            except (ValueError, TypeError):
                raise ValueError("Incorrect parameter n_clusters has value:"
                                 " {}. It should either be a single integer"
                                 " or an iterable with two integers:"
                                 " (n_row_clusters, n_column_clusters)")
        if self.n_components < 1:
            raise ValueError("Parameter n_components must be greater than 0,"
                             " but its value is {}".format(self.n_components))
        if self.n_best < 1:
            raise ValueError("Parameter n_best must be greater than 0,"
                             " but its value is {}".format(self.n_best))
        if self.n_best > self.n_components:
            raise ValueError("n_best cannot be larger than"
                             " n_components, but {} >  {}"
                             "".format(self.n_best, self.n_components))

    def _fit(self, X):
        n_sv = self.n_components
        if self.method == 'bistochastic':
            normalized_data = _bistochastic_normalize(X)
            n_sv += 1
        elif self.method == 'scale':
            normalized_data, _, _ = _scale_normalize(X)
            n_sv += 1
        elif self.method == 'log':
            normalized_data = _log_normalize(X)
        n_discard = 0 if self.method == 'log' else 1
        u, v = self._svd(normalized_data, n_sv, n_discard)
        ut = u.T
        vt = v.T

        try:
            n_row_clusters, n_col_clusters = self.n_clusters
        except TypeError:
            n_row_clusters = n_col_clusters = self.n_clusters

        best_ut = self._fit_best_piecewise(ut, self.n_best,
                                           n_row_clusters)

        best_vt = self._fit_best_piecewise(vt, self.n_best,
                                           n_col_clusters)

        self.row_labels_ = self._project_and_cluster(X, best_vt.T,
                                                     n_row_clusters)

        self.column_labels_ = self._project_and_cluster(X.T, best_ut.T,
                                                        n_col_clusters)

        self.rows_ = np.vstack(self.row_labels_ == label
                               for label in range(n_row_clusters)
                               for _ in range(n_col_clusters))
        self.columns_ = np.vstack(self.column_labels_ == label
                                  for _ in range(n_row_clusters)
                                  for label in range(n_col_clusters))

    def _fit_best_piecewise(self, vectors, n_best, n_clusters):
        """Find the ``n_best`` vectors that are best approximated by piecewise
        constant vectors.

        The piecewise vectors are found by k-means; the best is chosen
        according to Euclidean distance.

        """
        def make_piecewise(v):
            centroid, labels = self._k_means(v.reshape(-1, 1), n_clusters)
            return centroid[labels].ravel()
        piecewise_vectors = np.apply_along_axis(make_piecewise,
                                                axis=1, arr=vectors)
        dists = np.apply_along_axis(norm, axis=1,
                                    arr=(vectors - piecewise_vectors))
        result = vectors[np.argsort(dists)[:n_best]]
        return result

    def _project_and_cluster(self, data, vectors, n_clusters):
        """Project ``data`` to ``vectors`` and cluster the result."""
        projected = safe_sparse_dot(data, vectors)
        _, labels = self._k_means(projected, n_clusters)
        return labels
