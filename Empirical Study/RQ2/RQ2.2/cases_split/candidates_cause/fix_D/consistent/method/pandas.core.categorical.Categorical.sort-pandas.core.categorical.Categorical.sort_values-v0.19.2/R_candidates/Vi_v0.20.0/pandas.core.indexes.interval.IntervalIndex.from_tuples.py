    @classmethod
    def from_tuples(cls, data, closed='right', name=None, copy=False):
        """
        Construct an IntervalIndex from a list/array of tuples

        Parameters
        ----------
        data : array-like (1-dimensional)
            Array of tuples
        closed : {'left', 'right', 'both', 'neither'}, optional
            Whether the intervals are closed on the left-side, right-side, both
            or neither. Defaults to 'right'.
        name : object, optional
            Name to be stored in the index.
        copy : boolean, default False
            by-default copy the data, this is compat only and ignored

        Examples
        --------

        """
        left = []
        right = []
        for d in data:

            if isnull(d):
                left.append(np.nan)
                right.append(np.nan)
                continue

            l, r = d
            left.append(l)
            right.append(r)

        # TODO
        # if we have nulls and we previous had *only*
        # integer data, then we have changed the dtype

        return cls.from_arrays(left, right, closed, name=name, copy=False)
