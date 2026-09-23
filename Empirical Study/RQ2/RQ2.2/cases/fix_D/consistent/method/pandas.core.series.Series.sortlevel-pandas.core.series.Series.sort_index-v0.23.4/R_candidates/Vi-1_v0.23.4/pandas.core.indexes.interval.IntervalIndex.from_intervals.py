    @classmethod
    def from_intervals(cls, data, closed=None, name=None, copy=False,
                       dtype=None):
        """
        Construct an IntervalIndex from a 1d array of Interval objects

        .. deprecated:: 0.23.0

        Parameters
        ----------
        data : array-like (1-dimensional)
            Array of Interval objects. All intervals must be closed on the same
            sides.
        name : object, optional
            Name to be stored in the index.
        copy : boolean, default False
            by-default copy the data, this is compat only and ignored
        dtype : dtype or None, default None
            If None, dtype will be inferred

            .. versionadded:: 0.23.0

        Examples
        --------
        >>> pd.IntervalIndex.from_intervals([pd.Interval(0, 1),
        ...                                  pd.Interval(1, 2)])
        IntervalIndex([(0, 1], (1, 2]]
                      closed='right', dtype='interval[int64]')

        The generic Index constructor work identically when it infers an array
        of all intervals:

        >>> pd.Index([pd.Interval(0, 1), pd.Interval(1, 2)])
        IntervalIndex([(0, 1], (1, 2]]
                      closed='right', dtype='interval[int64]')

        See Also
        --------
        interval_range : Function to create a fixed frequency IntervalIndex
        IntervalIndex.from_arrays : Construct an IntervalIndex from a left and
                                    right array
        IntervalIndex.from_breaks : Construct an IntervalIndex from an array of
                                    splits
        IntervalIndex.from_tuples : Construct an IntervalIndex from a
                                    list/array of tuples
        """
        msg = ('IntervalIndex.from_intervals is deprecated and will be '
               'removed in a future version; use IntervalIndex(...) instead')
        warnings.warn(msg, FutureWarning, stacklevel=2)
        return cls(data, closed=closed, name=name, copy=copy, dtype=dtype)
