    @classmethod
    def from_tuples(cls, tuples, sortorder=None, names=None):
        """
        Convert list of tuples to MultiIndex.

        Parameters
        ----------
        tuples : list / sequence of tuple-likes
            Each tuple is the index of one row/column.
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
        MultiIndex.from_arrays : Convert list of arrays to MultiIndex.
        MultiIndex.from_product : Make a MultiIndex from cartesian product
                                  of iterables.
        MultiIndex.from_frame : Make a MultiIndex from a DataFrame.

        Examples
        --------
        >>> tuples = [(1, u'red'), (1, u'blue'),
        ...           (2, u'red'), (2, u'blue')]
        >>> pd.MultiIndex.from_tuples(tuples, names=('number', 'color'))
        MultiIndex(levels=[[1, 2], ['blue', 'red']],
                   codes=[[0, 0, 1, 1], [1, 0, 1, 0]],
                   names=['number', 'color'])
        """
        if not is_list_like(tuples):
            raise TypeError('Input must be a list / sequence of tuple-likes.')
        elif is_iterator(tuples):
            tuples = list(tuples)

        if len(tuples) == 0:
            if names is None:
                msg = 'Cannot infer number of levels from empty list'
                raise TypeError(msg)
            arrays = [[]] * len(names)
        elif isinstance(tuples, (np.ndarray, Index)):
            if isinstance(tuples, Index):
                tuples = tuples._values

            arrays = list(lib.tuples_to_object_array(tuples).T)
        elif isinstance(tuples, list):
            arrays = list(lib.to_object_array_tuples(tuples).T)
        else:
            arrays = lzip(*tuples)

        return MultiIndex.from_arrays(arrays, sortorder=sortorder, names=names)
