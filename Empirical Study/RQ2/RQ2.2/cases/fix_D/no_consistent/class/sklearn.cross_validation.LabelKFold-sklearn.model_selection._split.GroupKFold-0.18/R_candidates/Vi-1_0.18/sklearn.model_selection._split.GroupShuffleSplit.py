class GroupShuffleSplit(ShuffleSplit):
    '''Shuffle-Group(s)-Out cross-validation iterator

    Provides randomized train/test indices to split data according to a
    third-party provided group. This group information can be used to encode
    arbitrary domain specific stratifications of the samples as integers.

    For instance the groups could be the year of collection of the samples
    and thus allow for cross-validation against time-based splits.

    The difference between LeavePGroupsOut and GroupShuffleSplit is that
    the former generates splits using all subsets of size ``p`` unique groups,
    whereas GroupShuffleSplit generates a user-determined number of random
    test splits, each with a user-determined fraction of unique groups.

    For example, a less computationally intensive alternative to
    ``LeavePGroupsOut(p=10)`` would be
    ``GroupShuffleSplit(test_size=10, n_splits=100)``.

    Note: The parameters ``test_size`` and ``train_size`` refer to groups, and
    not to samples, as in ShuffleSplit.


    Parameters
    ----------
    n_splits : int (default 5)
        Number of re-shuffling & splitting iterations.

    test_size : float (default 0.2), int, or None
        If float, should be between 0.0 and 1.0 and represent the
        proportion of the groups to include in the test split. If
        int, represents the absolute number of test groups. If None,
        the value is automatically set to the complement of the train size.

    train_size : float, int, or None (default is None)
        If float, should be between 0.0 and 1.0 and represent the
        proportion of the groups to include in the train split. If
        int, represents the absolute number of train groups. If None,
        the value is automatically set to the complement of the test size.

    random_state : int or RandomState
        Pseudo-random number generator state used for random sampling.
    '''

    def __init__(self, n_splits=5, test_size=0.2, train_size=None,
                 random_state=None):
        super(GroupShuffleSplit, self).__init__(
            n_splits=n_splits,
            test_size=test_size,
            train_size=train_size,
            random_state=random_state)

    def _iter_indices(self, X, y, groups):
        if groups is None:
            raise ValueError("The groups parameter should not be None")
        classes, group_indices = np.unique(groups, return_inverse=True)
        for group_train, group_test in super(
                GroupShuffleSplit, self)._iter_indices(X=classes):
            # these are the indices of classes in the partition
            # invert them into data indices

            train = np.flatnonzero(np.in1d(group_indices, group_train))
            test = np.flatnonzero(np.in1d(group_indices, group_test))

            yield train, test
