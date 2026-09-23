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
        from pandas.core.categorical import Categorical

        if len(arrays) == 1:
            name = None if names is None else names[0]
            return Index(arrays[0], name=name)

        cats = [Categorical.from_array(arr) for arr in arrays]
        levels = [c.levels for c in cats]
        labels = [c.labels for c in cats]
        if names is None:
            names = [c.name for c in cats]

        return MultiIndex(levels=levels, labels=labels,
                          sortorder=sortorder, names=names,
                          verify_integrity=False)
