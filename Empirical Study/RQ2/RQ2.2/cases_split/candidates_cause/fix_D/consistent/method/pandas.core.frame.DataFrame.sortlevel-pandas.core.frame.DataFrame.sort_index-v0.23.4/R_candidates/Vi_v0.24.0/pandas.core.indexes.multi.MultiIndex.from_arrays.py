    @classmethod
    def from_arrays(cls, arrays, sortorder=None, names=None):
        """
        Convert arrays to MultiIndex.

        Parameters
        ----------
        arrays : list / sequence of array-likes
            Each array-like gives one level's value for each data point.
            len(arrays) is the number of levels.
        sortorder : int or None
            Level of sortedness (must be lexicographically sorted by that
            level).
        names : list / sequence of str, optional
            Names for the levels in the index.

        Returns
        -------
        index : MultiIndex

        See Also
        --------
        MultiIndex.from_tuples : Convert list of tuples to MultiIndex.
        MultiIndex.from_product : Make a MultiIndex from cartesian product
                                  of iterables.
        MultiIndex.from_frame : Make a MultiIndex from a DataFrame.

        Examples
        --------
        >>> arrays = [[1, 1, 2, 2], ['red', 'blue', 'red', 'blue']]
        >>> pd.MultiIndex.from_arrays(arrays, names=('number', 'color'))
        MultiIndex(levels=[[1, 2], ['blue', 'red']],
                   codes=[[0, 0, 1, 1], [1, 0, 1, 0]],
                   names=['number', 'color'])
        """
        if not is_list_like(arrays):
            raise TypeError("Input must be a list / sequence of array-likes.")
        elif is_iterator(arrays):
            arrays = list(arrays)

        # Check if lengths of all arrays are equal or not,
        # raise ValueError, if not
        for i in range(1, len(arrays)):
            if len(arrays[i]) != len(arrays[i - 1]):
                raise ValueError('all arrays must be same length')

        from pandas.core.arrays.categorical import _factorize_from_iterables

        codes, levels = _factorize_from_iterables(arrays)
        if names is None:
            names = [getattr(arr, "name", None) for arr in arrays]

        return MultiIndex(levels=levels, codes=codes, sortorder=sortorder,
                          names=names, verify_integrity=False)
