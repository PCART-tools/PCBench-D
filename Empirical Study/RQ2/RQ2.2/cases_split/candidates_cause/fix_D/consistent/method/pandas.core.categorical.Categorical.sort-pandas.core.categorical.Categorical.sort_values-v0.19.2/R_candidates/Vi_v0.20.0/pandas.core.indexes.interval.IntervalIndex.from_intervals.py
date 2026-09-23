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

        >>> IntervalIndex.from_intervals([Interval(0, 1), Interval(1, 2)])
        IntervalIndex(left=[0, 1],
                      right=[1, 2],
                      closed='right')

        The generic Index constructor work identically when it infers an array
        of all intervals:

        >>> Index([Interval(0, 1), Interval(1, 2)])
        IntervalIndex(left=[0, 1],
                      right=[1, 2],
                      closed='right')
        """
        data = np.asarray(data)
        left, right, closed = intervals_to_interval_bounds(data)
        return cls.from_arrays(left, right, closed, name=name, copy=False)
