    @classmethod
    def from_intervals(cls, data, name=None, copy=False):
        """
        Construct an IntervalIndex from a 1d array of Interval objects

        Parameters
        ----------
        data : array-like (1-dimensional)
            Array of Interval objects. All intervals must be closed on the same
            sides.
        name : object, optional
            Name to be stored in the index.
        copy : boolean, default False
            by-default copy the data, this is compat only and ignored

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
        data = np.asarray(data)
        left, right, closed = intervals_to_interval_bounds(data)
        return cls.from_arrays(left, right, closed, name=name, copy=False)
