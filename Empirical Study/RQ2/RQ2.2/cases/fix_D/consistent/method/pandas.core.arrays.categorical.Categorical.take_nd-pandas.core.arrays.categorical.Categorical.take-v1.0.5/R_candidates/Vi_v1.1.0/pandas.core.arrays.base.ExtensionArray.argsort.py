    def argsort(
        self, ascending: bool = True, kind: str = "quicksort", *args, **kwargs
    ) -> np.ndarray:
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
            Passed through to :func:`numpy.argsort`.

        Returns
        -------
        ndarray
            Array of indices that sort ``self``. If NaN values are contained,
            NaN values are placed at the end.

        See Also
        --------
        numpy.argsort : Sorting implementation used internally.
        """
        # Implementor note: You have two places to override the behavior of
        # argsort.
        # 1. _values_for_argsort : construct the values passed to np.argsort
        # 2. argsort : total control over sorting.
        ascending = nv.validate_argsort_with_ascending(ascending, args, kwargs)

        result = nargsort(self, kind=kind, ascending=ascending, na_position="last")
        return result
