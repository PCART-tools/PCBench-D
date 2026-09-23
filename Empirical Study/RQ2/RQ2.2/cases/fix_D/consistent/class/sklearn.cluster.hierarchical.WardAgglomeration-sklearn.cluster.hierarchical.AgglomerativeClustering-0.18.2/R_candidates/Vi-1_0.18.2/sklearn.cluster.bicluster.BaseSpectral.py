class BaseSpectral(six.with_metaclass(ABCMeta, BaseEstimator,
                                      BiclusterMixin)):
    """Base class for spectral biclustering."""

    @abstractmethod
    def __init__(self, n_clusters=3, svd_method="randomized",
                 n_svd_vecs=None, mini_batch=False, init="k-means++",
                 n_init=10, n_jobs=1, random_state=None):
        self.n_clusters = n_clusters
        self.svd_method = svd_method
        self.n_svd_vecs = n_svd_vecs
        self.mini_batch = mini_batch
        self.init = init
        self.n_init = n_init
        self.n_jobs = n_jobs
        self.random_state = random_state

    def _check_parameters(self):
        legal_svd_methods = ('randomized', 'arpack')
        if self.svd_method not in legal_svd_methods:
            raise ValueError("Unknown SVD method: '{0}'. svd_method must be"
                             " one of {1}.".format(self.svd_method,
                                                   legal_svd_methods))

    def fit(self, X):
        """Creates a biclustering for X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)

        """
        X = check_array(X, accept_sparse='csr', dtype=np.float64)
        self._check_parameters()
        self._fit(X)
        return self

    def _svd(self, array, n_components, n_discard):
        """Returns first `n_components` left and right singular
        vectors u and v, discarding the first `n_discard`.

        """
        if self.svd_method == 'randomized':
            kwargs = {}
            if self.n_svd_vecs is not None:
                kwargs['n_oversamples'] = self.n_svd_vecs
            u, _, vt = randomized_svd(array, n_components,
                                      random_state=self.random_state,
                                      **kwargs)

        elif self.svd_method == 'arpack':
            u, _, vt = svds(array, k=n_components, ncv=self.n_svd_vecs)
            if np.any(np.isnan(vt)):
                # some eigenvalues of A * A.T are negative, causing
                # sqrt() to be np.nan. This causes some vectors in vt
                # to be np.nan.
                A = safe_sparse_dot(array.T, array)
                random_state = check_random_state(self.random_state)
                # initialize with [-1,1] as in ARPACK
                v0 = random_state.uniform(-1, 1, A.shape[0])
                _, v = eigsh(A, ncv=self.n_svd_vecs, v0=v0)
                vt = v.T
            if np.any(np.isnan(u)):
                A = safe_sparse_dot(array, array.T)
                random_state = check_random_state(self.random_state)
                # initialize with [-1,1] as in ARPACK
                v0 = random_state.uniform(-1, 1, A.shape[0])
                _, u = eigsh(A, ncv=self.n_svd_vecs, v0=v0)

        assert_all_finite(u)
        assert_all_finite(vt)
        u = u[:, n_discard:]
        vt = vt[n_discard:]
        return u, vt.T

    def _k_means(self, data, n_clusters):
        if self.mini_batch:
            model = MiniBatchKMeans(n_clusters,
                                    init=self.init,
                                    n_init=self.n_init,
                                    random_state=self.random_state)
        else:
            model = KMeans(n_clusters, init=self.init,
                           n_init=self.n_init, n_jobs=self.n_jobs,
                           random_state=self.random_state)
        model.fit(data)
        centroid = model.cluster_centers_
        labels = model.labels_
        return centroid, labels
