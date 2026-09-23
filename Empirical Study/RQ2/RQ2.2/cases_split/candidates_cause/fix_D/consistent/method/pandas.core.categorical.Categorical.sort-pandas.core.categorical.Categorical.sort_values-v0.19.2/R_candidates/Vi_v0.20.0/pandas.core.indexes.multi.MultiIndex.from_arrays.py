    @classmethod
    def from_arrays(cls, arrays, sortorder=None, names=None):
        """
        Convert arrays to MultiIndex

        Parameters
        ----------
        arrays : list / sequence of array-likes
            Each array-like gives one level's value for each data point.
            len(arrays) is the number of levels.
        sortorder : int or None
            Level of sortedness (must be lexicographically sorted by that
            level)

        Returns
        -------
        index : MultiIndex

        Examples
        --------
        >>> arrays = [[1, 1, 2, 2], ['red', 'blue', 'red', 'blue']]
        >>> MultiIndex.from_arrays(arrays, names=('number', 'color'))

        See Also
        --------
        MultiIndex.from_tuples : Convert list of tuples to MultiIndex
        MultiIndex.from_product : Make a MultiIndex from cartesian product
                                  of iterables
        """
        if len(arrays) == 1:
            name = None if names is None else names[0]
            return Index(arrays[0], name=name)

        # Check if lengths of all arrays are equal or not,
        # raise ValueError, if not
        for i in range(1, len(arrays)):
            if len(arrays[i]) != len(arrays[i - 1]):
                raise ValueError('all arrays must be same length')

        from pandas.core.categorical import _factorize_from_iterables

        labels, levels = _factorize_from_iterables(arrays)
        if names is None:
            names = [getattr(arr, "name", None) for arr in arrays]

        return MultiIndex(levels=levels, labels=labels, sortorder=sortorder,
                          names=names, verify_integrity=False)
