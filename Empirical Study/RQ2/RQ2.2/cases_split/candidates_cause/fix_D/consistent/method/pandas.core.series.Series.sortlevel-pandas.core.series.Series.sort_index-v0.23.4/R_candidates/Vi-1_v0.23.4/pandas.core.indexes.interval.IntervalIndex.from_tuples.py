    @classmethod
    def from_tuples(cls, data, closed='right', name=None, copy=False,
                    dtype=None):
        """
        Construct an IntervalIndex from a list/array of tuples

        Parameters
        ----------
        data : array-like (1-dimensional)
            Array of tuples
        closed : {'left', 'right', 'both', 'neither'}, default 'right'
            Whether the intervals are closed on the left-side, right-side, both
            or neither.
        name : object, optional
            Name to be stored in the index.
        copy : boolean, default False
            by-default copy the data, this is compat only and ignored
        dtype : dtype or None, default None
            If None, dtype will be inferred

            .. versionadded:: 0.23.0

        Examples
        --------
        >>>  pd.IntervalIndex.from_tuples([(0, 1), (1, 2)])
        IntervalIndex([(0, 1], (1, 2]],
                      closed='right', dtype='interval[int64]')

        See Also
        --------
        interval_range : Function to create a fixed frequency IntervalIndex
        IntervalIndex.from_arrays : Construct an IntervalIndex from a left and
                                    right array
        IntervalIndex.from_breaks : Construct an IntervalIndex from an array of
                                    splits
        """
        if len(data):
            left, right = [], []
        else:
            left = right = data

        for d in data:
            if isna(d):
                lhs = rhs = np.nan
            else:
                try:
                    # need list of length 2 tuples, e.g. [(0, 1), (1, 2), ...]
                    lhs, rhs = d
                except ValueError:
                    msg = ('IntervalIndex.from_tuples requires tuples of '
                           'length 2, got {tpl}').format(tpl=d)
                    raise ValueError(msg)
                except TypeError:
                    msg = ('IntervalIndex.from_tuples received an invalid '
                           'item, {tpl}').format(tpl=d)
                    raise TypeError(msg)
            left.append(lhs)
            right.append(rhs)

        return cls.from_arrays(left, right, closed, name=name, copy=False,
                               dtype=dtype)
