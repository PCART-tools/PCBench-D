class Birch(BaseEstimator, TransformerMixin, ClusterMixin):
    """Implements the Birch clustering algorithm.

    Every new sample is inserted into the root of the Clustering Feature
    Tree. It is then clubbed together with the subcluster that has the
    centroid closest to the new sample. This is done recursively till it
    ends up at the subcluster of the leaf of the tree has the closest centroid.

    Read more in the :ref:`User Guide <birch>`.

    Parameters
    ----------
    threshold : float, default 0.5
        The radius of the subcluster obtained by merging a new sample and the
        closest subcluster should be lesser than the threshold. Otherwise a new
        subcluster is started.

    branching_factor : int, default 50
        Maximum number of CF subclusters in each node. If a new samples enters
        such that the number of subclusters exceed the branching_factor then
        the node has to be split. The corresponding parent also has to be
        split and if the number of subclusters in the parent is greater than
        the branching factor, then it has to be split recursively.

    n_clusters : int, instance of sklearn.cluster model, default None
        Number of clusters after the final clustering step, which treats the
        subclusters from the leaves as new samples. By default, this final
        clustering step is not performed and the subclusters are returned
        as they are. If a model is provided, the model is fit treating
        the subclusters as new samples and the initial data is mapped to the
        label of the closest subcluster. If an int is provided, the model
        fit is AgglomerativeClustering with n_clusters set to the int.

    compute_labels : bool, default True
        Whether or not to compute labels for each fit.

    copy : bool, default True
        Whether or not to make a copy of the given data. If set to False,
        the initial data will be overwritten.

    Attributes
    ----------
    root_ : _CFNode
        Root of the CFTree.

    dummy_leaf_ : _CFNode
        Start pointer to all the leaves.

    subcluster_centers_ : ndarray,
        Centroids of all subclusters read directly from the leaves.

    subcluster_labels_ : ndarray,
        Labels assigned to the centroids of the subclusters after
        they are clustered globally.

    labels_ : ndarray, shape (n_samples,)
        Array of labels assigned to the input data.
        if partial_fit is used instead of fit, they are assigned to the
        last batch of data.

    Examples
    --------
    >>> from sklearn.cluster import Birch
    >>> X = [[0, 1], [0.3, 1], [-0.3, 1], [0, -1], [0.3, -1], [-0.3, -1]]
    >>> brc = Birch(branching_factor=50, n_clusters=None, threshold=0.5,
    ... compute_labels=True)
    >>> brc.fit(X)
    Birch(branching_factor=50, compute_labels=True, copy=True, n_clusters=None,
       threshold=0.5)
    >>> brc.predict(X)
    array([0, 0, 0, 1, 1, 1])

    References
    ----------
    * Tian Zhang, Raghu Ramakrishnan, Maron Livny
      BIRCH: An efficient data clustering method for large databases.
      http://www.cs.sfu.ca/CourseCentral/459/han/papers/zhang96.pdf

    * Roberto Perdisci
      JBirch - Java implementation of BIRCH clustering algorithm
      https://code.google.com/p/jbirch/
    """

    def __init__(self, threshold=0.5, branching_factor=50, n_clusters=3,
                 compute_labels=True, copy=True):
        self.threshold = threshold
        self.branching_factor = branching_factor
        self.n_clusters = n_clusters
        self.compute_labels = compute_labels
        self.copy = copy

    def fit(self, X, y=None):
        """
        Build a CF Tree for the input data.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Input data.
        """
        self.fit_, self.partial_fit_ = True, False
        return self._fit(X)

    def _fit(self, X):
        X = check_array(X, accept_sparse='csr', copy=self.copy)
        threshold = self.threshold
        branching_factor = self.branching_factor

        if branching_factor <= 1:
            raise ValueError("Branching_factor should be greater than one.")
        n_samples, n_features = X.shape

        # If partial_fit is called for the first time or fit is called, we
        # start a new tree.
        partial_fit = getattr(self, 'partial_fit_')
        has_root = getattr(self, 'root_', None)
        if getattr(self, 'fit_') or (partial_fit and not has_root):
            # The first root is the leaf. Manipulate this object throughout.
            self.root_ = _CFNode(threshold, branching_factor, is_leaf=True,
                                 n_features=n_features)

            # To enable getting back subclusters.
            self.dummy_leaf_ = _CFNode(threshold, branching_factor,
                                       is_leaf=True, n_features=n_features)
            self.dummy_leaf_.next_leaf_ = self.root_
            self.root_.prev_leaf_ = self.dummy_leaf_

        # Cannot vectorize. Enough to convince to use cython.
        if not sparse.issparse(X):
            iter_func = iter
        else:
            iter_func = _iterate_sparse_X

        for sample in iter_func(X):
            subcluster = _CFSubcluster(linear_sum=sample)
            split = self.root_.insert_cf_subcluster(subcluster)

            if split:
                new_subcluster1, new_subcluster2 = _split_node(
                    self.root_, threshold, branching_factor)
                del self.root_
                self.root_ = _CFNode(threshold, branching_factor,
                                     is_leaf=False,
                                     n_features=n_features)
                self.root_.append_subcluster(new_subcluster1)
                self.root_.append_subcluster(new_subcluster2)

        centroids = np.concatenate([
            leaf.centroids_ for leaf in self._get_leaves()])
        self.subcluster_centers_ = centroids

        self._global_clustering(X)
        return self

    def _get_leaves(self):
        """
        Retrieve the leaves of the CF Node.

        Returns
        -------
        leaves: array-like
            List of the leaf nodes.
        """
        leaf_ptr = self.dummy_leaf_.next_leaf_
        leaves = []
        while leaf_ptr is not None:
            leaves.append(leaf_ptr)
            leaf_ptr = leaf_ptr.next_leaf_
        return leaves

    def partial_fit(self, X=None, y=None):
        """
        Online learning. Prevents rebuilding of CFTree from scratch.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features), None
            Input data. If X is not provided, only the global clustering
            step is done.
        """
        self.partial_fit_, self.fit_ = True, False
        if X is None:
            # Perform just the final global clustering step.
            self._global_clustering()
            return self
        else:
            self._check_fit(X)
            return self._fit(X)

    def _check_fit(self, X):
        is_fitted = hasattr(self, 'subcluster_centers_')

        # Called by partial_fit, before fitting.
        has_partial_fit = hasattr(self, 'partial_fit_')

        # Should raise an error if one does not fit before predicting.
        if not (is_fitted or has_partial_fit):
            raise NotFittedError("Fit training data before predicting")

        if is_fitted and X.shape[1] != self.subcluster_centers_.shape[1]:
            raise ValueError(
                "Training data and predicted data do "
                "not have same number of features.")

    def predict(self, X):
        """
        Predict data using the ``centroids_`` of subclusters.

        Avoid computation of the row norms of X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Input data.

        Returns
        -------
        labels: ndarray, shape(n_samples)
            Labelled data.
        """
        X = check_array(X, accept_sparse='csr')
        self._check_fit(X)
        reduced_distance = safe_sparse_dot(X, self.subcluster_centers_.T)
        reduced_distance *= -2
        reduced_distance += self._subcluster_norms
        return self.subcluster_labels_[np.argmin(reduced_distance, axis=1)]

    def transform(self, X, y=None):
        """
        Transform X into subcluster centroids dimension.

        Each dimension represents the distance from the sample point to each
        cluster centroid.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_samples, n_features)
            Input data.

        Returns
        -------
        X_trans : {array-like, sparse matrix}, shape (n_samples, n_clusters)
            Transformed data.
        """
        check_is_fitted(self, 'subcluster_centers_')
        return euclidean_distances(X, self.subcluster_centers_)

    def _global_clustering(self, X=None):
        """
        Global clustering for the subclusters obtained after fitting
        """
        clusterer = self.n_clusters
        centroids = self.subcluster_centers_
        compute_labels = (X is not None) and self.compute_labels

        # Preprocessing for the global clustering.
        not_enough_centroids = False
        if isinstance(clusterer, int):
            clusterer = AgglomerativeClustering(
                n_clusters=self.n_clusters)
            # There is no need to perform the global clustering step.
            if len(centroids) < self.n_clusters:
                not_enough_centroids = True
        elif (clusterer is not None and not
              hasattr(clusterer, 'fit_predict')):
            raise ValueError("n_clusters should be an instance of "
                             "ClusterMixin or an int")

        # To use in predict to avoid recalculation.
        self._subcluster_norms = row_norms(
            self.subcluster_centers_, squared=True)

        if clusterer is None or not_enough_centroids:
            self.subcluster_labels_ = np.arange(len(centroids))
            if not_enough_centroids:
                warnings.warn(
                    "Number of subclusters found (%d) by Birch is less "
                    "than (%d). Decrease the threshold."
                    % (len(centroids), self.n_clusters))
        else:
            # The global clustering step that clusters the subclusters of
            # the leaves. It assumes the centroids of the subclusters as
            # samples and finds the final centroids.
            self.subcluster_labels_ = clusterer.fit_predict(
                self.subcluster_centers_)

        if compute_labels:
            self.labels_ = self.predict(X)
