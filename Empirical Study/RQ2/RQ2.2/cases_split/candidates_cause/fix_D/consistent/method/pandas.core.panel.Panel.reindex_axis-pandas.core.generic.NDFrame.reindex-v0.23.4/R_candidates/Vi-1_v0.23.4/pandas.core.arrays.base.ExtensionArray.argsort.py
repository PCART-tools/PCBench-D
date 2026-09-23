    def argsort(self, ascending=True, kind='quicksort', *args, **kwargs):
        """
        Return the indices that would sort this array.

        Parameters
        ----------
        ascending : bool, default True
            Whether the indices should result in an ascending
            or descending sort.
        kind : {'quicksort', 'mergesort', 'heapsort'}, optional
            Sorting algorithm.
        *args, **kwargs:
            passed through to :func:`numpy.argsort`.

        Returns
        -------
        index_array : ndarray
            Array of indices that sort ``self``.

        See Also
        --------
        numpy.argsort : Sorting implementation used internally.
        """
        # Implementor note: You have two places to override the behavior of
        # argsort.
        # 1. _values_for_argsort : construct the values passed to np.argsort
        # 2. argsort : total control over sorting.
        ascending = nv.validate_argsort_with_ascending(ascending, args, kwargs)
        values = self._values_for_argsort()
        result = np.argsort(values, kind=kind, **kwargs)
        if not ascending:
            result = result[::-1]
        return result
