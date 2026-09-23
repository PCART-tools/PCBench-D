    @classmethod
    def from_tuples(cls, tuples, sortorder=None, names=None):
        """
        Convert list of tuples to MultiIndex

        Parameters
        ----------
        tuples : array-like
        sortorder : int or None
            Level of sortedness (must be lexicographically sorted by that
            level)

        Returns
        -------
        index : MultiIndex
        """
        if len(tuples) == 0:
            # I think this is right? Not quite sure...
            raise TypeError('Cannot infer number of levels from empty list')

        if isinstance(tuples, np.ndarray):
            if isinstance(tuples, Index):
                tuples = tuples.values

            arrays = list(lib.tuples_to_object_array(tuples).T)
        elif isinstance(tuples, list):
            arrays = list(lib.to_object_array_tuples(tuples).T)
        else:
            arrays = lzip(*tuples)

        return MultiIndex.from_arrays(arrays, sortorder=sortorder,
                                      names=names)
