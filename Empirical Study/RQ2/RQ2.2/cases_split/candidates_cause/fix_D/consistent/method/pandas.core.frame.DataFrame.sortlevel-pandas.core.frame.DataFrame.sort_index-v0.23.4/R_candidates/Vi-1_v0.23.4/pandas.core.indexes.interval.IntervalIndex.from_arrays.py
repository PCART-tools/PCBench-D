    @classmethod
    def from_arrays(cls, left, right, closed='right', name=None, copy=False,
                    dtype=None):
        """
        Construct from two arrays defining the left and right bounds.

        Parameters
        ----------
        left : array-like (1-dimensional)
            Left bounds for each interval.
        right : array-like (1-dimensional)
            Right bounds for each interval.
        closed : {'left', 'right', 'both', 'neither'}, default 'right'
            Whether the intervals are closed on the left-side, right-side, both
            or neither.
        name : object, optional
            Name to be stored in the index.
        copy : boolean, default False
            Copy the data.
        dtype : dtype, optional
            If None, dtype will be inferred.

            .. versionadded:: 0.23.0

        Returns
        -------
        index : IntervalIndex

        Notes
        -----
        Each element of `left` must be less than or equal to the `right`
        element at the same position. If an element is missing, it must be
        missing in both `left` and `right`. A TypeError is raised when
        using an unsupported type for `left` or `right`. At the moment,
        'category', 'object', and 'string' subtypes are not supported.

        Raises
        ------
        ValueError
            When a value is missing in only one of `left` or `right`.
            When a value in `left` is greater than the corresponding value
            in `right`.

        See Also
        --------
        interval_range : Function to create a fixed frequency IntervalIndex.
        IntervalIndex.from_breaks : Construct an IntervalIndex from an array of
            splits.
        IntervalIndex.from_tuples : Construct an IntervalIndex from a
            list/array of tuples.

        Examples
        --------
        >>> pd.IntervalIndex.from_arrays([0, 1, 2], [1, 2, 3])
        IntervalIndex([(0, 1], (1, 2], (2, 3]]
                      closed='right',
                      dtype='interval[int64]')

        If you want to segment different groups of people based on
        ages, you can apply the method as follows:

        >>> ages = pd.IntervalIndex.from_arrays([0, 2, 13],
        ...                                     [2, 13, 19], closed='left')
        >>> ages
        IntervalIndex([[0, 2), [2, 13), [13, 19)]
                      closed='left',
                      dtype='interval[int64]')
        >>> s = pd.Series(['baby', 'kid', 'teen'], ages)
        >>> s
        [0, 2)      baby
        [2, 13)      kid
        [13, 19)    teen
        dtype: object

        Values may be missing, but they must be missing in both arrays.

        >>> pd.IntervalIndex.from_arrays([0, np.nan, 13],
        ...                              [2, np.nan, 19])
        IntervalIndex([(0.0, 2.0], nan, (13.0, 19.0]]
                      closed='right',
                      dtype='interval[float64]')
        """
        left = maybe_convert_platform_interval(left)
        right = maybe_convert_platform_interval(right)

        return cls._simple_new(left, right, closed, name=name, copy=copy,
                               dtype=dtype, verify_integrity=True)
