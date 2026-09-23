    @classmethod
    def from_arrays(cls, left, right, closed='right', name=None, copy=False):
        """
        Construct an IntervalIndex from a a left and right array

        Parameters
        ----------
        left : array-like (1-dimensional)
            Left bounds for each interval.
        right : array-like (1-dimensional)
            Right bounds for each interval.
        closed : {'left', 'right', 'both', 'neither'}, optional
            Whether the intervals are closed on the left-side, right-side, both
            or neither. Defaults to 'right'.
        name : object, optional
            Name to be stored in the index.
        copy : boolean, default False
            copy the data

        Examples
        --------
        >>> pd.IntervalIndex.from_arrays([0, 1, 2], [1, 2, 3])
        IntervalIndex([(0, 1], (1, 2], (2, 3]]
                      closed='right',
                      dtype='interval[int64]')

        See Also
        --------
        interval_range : Function to create a fixed frequency IntervalIndex
        IntervalIndex.from_breaks : Construct an IntervalIndex from an array of
                                    splits
        IntervalIndex.from_intervals : Construct an IntervalIndex from an array
                                       of Interval objects
        IntervalIndex.from_tuples : Construct an IntervalIndex from a
                                    list/array of tuples
        """
        left = np.asarray(left)
        right = np.asarray(right)
        return cls._simple_new(left, right, closed, name=name,
                               copy=copy, verify_integrity=True)
