class LeavePLabelOut(_PartitionIterator):
    """Leave-P-Label_Out cross-validation iterator

    Provides train/test indices to split data according to a third-party
    provided label. This label information can be used to encode arbitrary
    domain specific stratifications of the samples as integers.

    For instance the labels could be the year of collection of the samples
    and thus allow for cross-validation against time-based splits.

    The difference between LeavePLabelOut and LeaveOneLabelOut is that
    the former builds the test sets with all the samples assigned to
    ``p`` different values of the labels while the latter uses samples
    all assigned the same labels.

    Read more in the :ref:`User Guide <cross_validation>`.

    Parameters
    ----------
    labels : array-like of int with shape (n_samples,)
        Arbitrary domain-specific stratification of the data to be used
        to draw the splits.

    p : int
        Number of samples to leave out in the test split.

    Examples
    --------
    >>> from sklearn import cross_validation
    >>> X = np.array([[1, 2], [3, 4], [5, 6]])
    >>> y = np.array([1, 2, 1])
    >>> labels = np.array([1, 2, 3])
    >>> lpl = cross_validation.LeavePLabelOut(labels, p=2)
    >>> len(lpl)
    3
    >>> print(lpl)
    sklearn.cross_validation.LeavePLabelOut(labels=[1 2 3], p=2)
    >>> for train_index, test_index in lpl:
    ...    print("TRAIN:", train_index, "TEST:", test_index)
    ...    X_train, X_test = X[train_index], X[test_index]
    ...    y_train, y_test = y[train_index], y[test_index]
    ...    print(X_train, X_test, y_train, y_test)
    TRAIN: [2] TEST: [0 1]
    [[5 6]] [[1 2]
     [3 4]] [1] [1 2]
    TRAIN: [1] TEST: [0 2]
    [[3 4]] [[1 2]
     [5 6]] [2] [1 1]
    TRAIN: [0] TEST: [1 2]
    [[1 2]] [[3 4]
     [5 6]] [1] [2 1]

    See also
    --------
    LabelKFold: K-fold iterator variant with non-overlapping labels.
    """

    def __init__(self, labels, p):
        # We make a copy of labels to avoid side-effects during iteration
        super(LeavePLabelOut, self).__init__(len(labels))
        self.labels = np.array(labels, copy=True)
        self.unique_labels = np.unique(labels)
        self.n_unique_labels = len(self.unique_labels)
        self.p = p

    def _iter_test_masks(self):
        comb = combinations(range(self.n_unique_labels), self.p)
        for idx in comb:
            test_index = self._empty_mask()
            idx = np.array(idx)
            for l in self.unique_labels[idx]:
                test_index[self.labels == l] = True
            yield test_index

    def __repr__(self):
        return '%s.%s(labels=%s, p=%s)' % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.labels,
            self.p,
        )

    def __len__(self):
        return int(factorial(self.n_unique_labels) /
                   factorial(self.n_unique_labels - self.p) /
                   factorial(self.p))
