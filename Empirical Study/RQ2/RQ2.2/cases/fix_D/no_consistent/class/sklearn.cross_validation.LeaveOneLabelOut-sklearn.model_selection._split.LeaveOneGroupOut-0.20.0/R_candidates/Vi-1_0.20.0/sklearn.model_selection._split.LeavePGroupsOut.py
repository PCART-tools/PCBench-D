class LeavePGroupsOut(BaseCrossValidator):
    """Leave P Group(s) Out cross-validator

    Provides train/test indices to split data according to a third-party
    provided group. This group information can be used to encode arbitrary
    domain specific stratifications of the samples as integers.

    For instance the groups could be the year of collection of the samples
    and thus allow for cross-validation against time-based splits.

    The difference between LeavePGroupsOut and LeaveOneGroupOut is that
    the former builds the test sets with all the samples assigned to
    ``p`` different values of the groups while the latter uses samples
    all assigned the same groups.

    Read more in the :ref:`User Guide <cross_validation>`.

    Parameters
    ----------
    n_groups : int
        Number of groups (``p``) to leave out in the test split.

    Examples
    --------
    >>> from sklearn.model_selection import LeavePGroupsOut
    >>> X = np.array([[1, 2], [3, 4], [5, 6]])
    >>> y = np.array([1, 2, 1])
    >>> groups = np.array([1, 2, 3])
    >>> lpgo = LeavePGroupsOut(n_groups=2)
    >>> lpgo.get_n_splits(X, y, groups)
    3
    >>> lpgo.get_n_splits(groups=groups)  # 'groups' is always required
    3
    >>> print(lpgo)
    LeavePGroupsOut(n_groups=2)
    >>> for train_index, test_index in lpgo.split(X, y, groups):
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
    GroupKFold: K-fold iterator variant with non-overlapping groups.
    """

    def __init__(self, n_groups):
        self.n_groups = n_groups

    def _iter_test_masks(self, X, y, groups):
        if groups is None:
            raise ValueError("The 'groups' parameter should not be None.")
        groups = check_array(groups, copy=True, ensure_2d=False, dtype=None)
        unique_groups = np.unique(groups)
        if self.n_groups >= len(unique_groups):
            raise ValueError(
                "The groups parameter contains fewer than (or equal to) "
                "n_groups (%d) numbers of unique groups (%s). LeavePGroupsOut "
                "expects that at least n_groups + 1 (%d) unique groups be "
                "present" % (self.n_groups, unique_groups, self.n_groups + 1))
        combi = combinations(range(len(unique_groups)), self.n_groups)
        for indices in combi:
            test_index = np.zeros(_num_samples(X), dtype=np.bool)
            for l in unique_groups[np.array(indices)]:
                test_index[groups == l] = True
            yield test_index

    def get_n_splits(self, X=None, y=None, groups=None):
        """Returns the number of splitting iterations in the cross-validator

        Parameters
        ----------
        X : object, optional
            Always ignored, exists for compatibility.

        y : object, optional
            Always ignored, exists for compatibility.

        groups : array-like, with shape (n_samples,), optional
            Group labels for the samples used while splitting the dataset into
            train/test set. This 'groups' parameter must always be specified to
            calculate the number of splits, though the other parameters can be
            omitted.

        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """
        if groups is None:
            raise ValueError("The 'groups' parameter should not be None.")
        groups = check_array(groups, ensure_2d=False, dtype=None)
        return int(comb(len(np.unique(groups)), self.n_groups, exact=True))
