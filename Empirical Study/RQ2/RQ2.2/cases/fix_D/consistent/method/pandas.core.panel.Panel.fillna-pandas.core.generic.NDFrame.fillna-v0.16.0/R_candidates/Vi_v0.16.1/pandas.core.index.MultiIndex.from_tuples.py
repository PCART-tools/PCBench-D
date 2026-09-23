    @classmethod
    def from_tuples(cls, tuples, sortorder=None, names=None):
        """
        Convert list of tuples to MultiIndex

        Parameters
        ----------
        tuples : list / sequence of tuple-likes
            Each tuple is the index of one row/column.
        sortorder : int or None
            Level of sortedness (must be lexicographically sorted by that
            level)

        Returns
        -------
        index : MultiIndex

        Examples
        --------
        >>> tuples = [(1, u'red'), (1, u'blue'),
                      (2, u'red'), (2, u'blue')]
        >>> MultiIndex.from_tuples(tuples, names=('number', 'color'))

        See Also
        --------
        MultiIndex.from_arrays : Convert list of arrays to MultiIndex
        MultiIndex.from_product : Make a MultiIndex from cartesian product
                                  of iterables
        """
        if len(tuples) == 0:
            # I think this is right? Not quite sure...
            raise TypeError('Cannot infer number of levels from empty list')

        if isinstance(tuples, (np.ndarray, Index)):
            if isinstance(tuples, Index):
                tuples = tuples.values

            arrays = list(lib.tuples_to_object_array(tuples).T)
        elif isinstance(tuples, list):
            arrays = list(lib.to_object_array_tuples(tuples).T)
        else:
            arrays = lzip(*tuples)

        return MultiIndex.from_arrays(arrays, sortorder=sortorder,
                                      names=names)
