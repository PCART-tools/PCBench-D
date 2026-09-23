    def _internal_get_values(self) -> np.ndarray:
        """
        Return an ndarray after converting sparse values to dense.

        This is the same as ``.values`` for non-sparse data. For sparse
        data contained in a `SparseArray`, the data are first
        converted to a dense representation.

        Returns
        -------
        numpy.ndarray
            Numpy representation of DataFrame.

        See Also
        --------
        values : Numpy representation of DataFrame.
        SparseArray : Container for sparse data.
        """
        return self.values
