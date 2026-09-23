class LabelKFold(_BaseKFold):
    """K-fold iterator variant with non-overlapping labels.

    The same label will not appear in two different folds (the number of
    distinct labels has to be at least equal to the number of folds).

    The folds are approximately balanced in the sense that the number of
    distinct labels is approximately the same in each fold.

    .. versionadded:: 0.17

    Parameters
    ----------
    labels : array-like with shape (n_samples, )
        Contains a label for each sample.
        The folds are built so that the same label does not appear in two
        different folds.

    n_folds : int, default=3
        Number of folds. Must be at least 2.

    Examples
    --------
    >>> from sklearn.cross_validation import LabelKFold
    >>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    >>> y = np.array([1, 2, 3, 4])
    >>> labels = np.array([0, 0, 2, 2])
    >>> label_kfold = LabelKFold(labels, n_folds=2)
    >>> len(label_kfold)
    2
    >>> print(label_kfold)
    sklearn.cross_validation.LabelKFold(n_labels=4, n_folds=2)
    >>> for train_index, test_index in label_kfold:
    ...     print("TRAIN:", train_index, "TEST:", test_index)
    ...     X_train, X_test = X[train_index], X[test_index]
    ...     y_train, y_test = y[train_index], y[test_index]
    ...     print(X_train, X_test, y_train, y_test)
    ...
    TRAIN: [0 1] TEST: [2 3]
    [[1 2]
     [3 4]] [[5 6]
     [7 8]] [1 2] [3 4]
    TRAIN: [2 3] TEST: [0 1]
    [[5 6]
     [7 8]] [[1 2]
     [3 4]] [3 4] [1 2]

    See also
    --------
    LeaveOneLabelOut for splitting the data according to explicit,
    domain-specific stratification of the dataset.
    """
    def __init__(self, labels, n_folds=3):
        super(LabelKFold, self).__init__(len(labels), n_folds,
                                         shuffle=False, random_state=None)

        unique_labels, labels = np.unique(labels, return_inverse=True)
        n_labels = len(unique_labels)

        if n_folds > n_labels:
            raise ValueError(
                    ("Cannot have number of folds n_folds={0} greater"
                     " than the number of labels: {1}.").format(n_folds,
                                                                n_labels))

        # Weight labels by their number of occurences
        n_samples_per_label = np.bincount(labels)

        # Distribute the most frequent labels first
        indices = np.argsort(n_samples_per_label)[::-1]
        n_samples_per_label = n_samples_per_label[indices]

        # Total weight of each fold
        n_samples_per_fold = np.zeros(n_folds)

        # Mapping from label index to fold index
        label_to_fold = np.zeros(len(unique_labels))

        # Distribute samples by adding the largest weight to the lightest fold
        for label_index, weight in enumerate(n_samples_per_label):
            lightest_fold = np.argmin(n_samples_per_fold)
            n_samples_per_fold[lightest_fold] += weight
            label_to_fold[indices[label_index]] = lightest_fold

        self.idxs = label_to_fold[labels]

    def _iter_test_indices(self):
        for f in range(self.n_folds):
            yield np.where(self.idxs == f)[0]

    def __repr__(self):
        return '{0}.{1}(n_labels={2}, n_folds={3})'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.n,
            self.n_folds,
        )

    def __len__(self):
        return self.n_folds
