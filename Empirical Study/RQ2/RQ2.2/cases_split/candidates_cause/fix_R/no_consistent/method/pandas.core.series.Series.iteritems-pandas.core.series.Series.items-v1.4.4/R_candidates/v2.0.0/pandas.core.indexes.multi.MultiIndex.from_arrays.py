    @classmethod
    def from_arrays(
        cls,
        arrays,
        sortorder=None,
        names: Sequence[Hashable] | Hashable | lib.NoDefault = lib.no_default,
    ) -> MultiIndex:
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
        MultiIndex

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
        MultiIndex([(1,  'red'),
                    (1, 'blue'),
                    (2,  'red'),
                    (2, 'blue')],
                   names=['number', 'color'])
        """
        error_msg = "Input must be a list / sequence of array-likes."
        if not is_list_like(arrays):
            raise TypeError(error_msg)
        if is_iterator(arrays):
            arrays = list(arrays)

        # Check if elements of array are list-like
        for array in arrays:
            if not is_list_like(array):
                raise TypeError(error_msg)

        # Check if lengths of all arrays are equal or not,
        # raise ValueError, if not
        for i in range(1, len(arrays)):
            if len(arrays[i]) != len(arrays[i - 1]):
                raise ValueError("all arrays must be same length")

        codes, levels = factorize_from_iterables(arrays)
        if names is lib.no_default:
            names = [getattr(arr, "name", None) for arr in arrays]

        return cls(
            levels=levels,
            codes=codes,
            sortorder=sortorder,
            names=names,
            verify_integrity=False,
        )
