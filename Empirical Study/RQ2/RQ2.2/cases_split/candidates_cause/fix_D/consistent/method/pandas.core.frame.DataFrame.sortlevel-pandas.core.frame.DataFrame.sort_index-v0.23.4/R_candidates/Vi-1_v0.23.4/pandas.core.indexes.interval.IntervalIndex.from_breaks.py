    @classmethod
    def from_breaks(cls, breaks, closed='right', name=None, copy=False,
                    dtype=None):
        """
        Construct an IntervalIndex from an array of splits

        Parameters
        ----------
        breaks : array-like (1-dimensional)
            Left and right bounds for each interval.
        closed : {'left', 'right', 'both', 'neither'}, default 'right'
            Whether the intervals are closed on the left-side, right-side, both
            or neither.
        name : object, optional
            Name to be stored in the index.
        copy : boolean, default False
            copy the data
        dtype : dtype or None, default None
            If None, dtype will be inferred

            .. versionadded:: 0.23.0

        Examples
        --------
        >>> pd.IntervalIndex.from_breaks([0, 1, 2, 3])
        IntervalIndex([(0, 1], (1, 2], (2, 3]]
                      closed='right',
                      dtype='interval[int64]')

        See Also
        --------
        interval_range : Function to create a fixed frequency IntervalIndex
        IntervalIndex.from_arrays : Construct an IntervalIndex from a left and
                                    right array
        IntervalIndex.from_tuples : Construct an IntervalIndex from a
                                    list/array of tuples
        """
        breaks = maybe_convert_platform_interval(breaks)

        return cls.from_arrays(breaks[:-1], breaks[1:], closed,
                               name=name, copy=copy, dtype=dtype)
