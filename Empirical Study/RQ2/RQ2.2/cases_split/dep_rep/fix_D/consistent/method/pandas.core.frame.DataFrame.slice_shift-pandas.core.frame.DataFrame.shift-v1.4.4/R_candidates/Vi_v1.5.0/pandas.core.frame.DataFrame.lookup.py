    def lookup(
        self, row_labels: Sequence[IndexLabel], col_labels: Sequence[IndexLabel]
    ) -> np.ndarray:
        """
        Label-based "fancy indexing" function for DataFrame.

        .. deprecated:: 1.2.0
            DataFrame.lookup is deprecated,
            use pandas.factorize and NumPy indexing instead.
            For further details see
            :ref:`Looking up values by index/column labels <indexing.lookup>`.

        Given equal-length arrays of row and column labels, return an
        array of the values corresponding to each (row, col) pair.

        Parameters
        ----------
        row_labels : sequence
            The row labels to use for lookup.
        col_labels : sequence
            The column labels to use for lookup.

        Returns
        -------
        numpy.ndarray
            The found values.
        """
        msg = (
            "The 'lookup' method is deprecated and will be "
            "removed in a future version. "
            "You can use DataFrame.melt and DataFrame.loc "
            "as a substitute."
        )
        warnings.warn(
            msg, FutureWarning, stacklevel=find_stack_level(inspect.currentframe())
        )

        n = len(row_labels)
        if n != len(col_labels):
            raise ValueError("Row labels must have same size as column labels")
        if not (self.index.is_unique and self.columns.is_unique):
            # GH#33041
            raise ValueError("DataFrame.lookup requires unique index and columns")

        thresh = 1000
        if not self._is_mixed_type or n > thresh:
            values = self.values
            ridx = self.index.get_indexer(row_labels)
            cidx = self.columns.get_indexer(col_labels)
            if (ridx == -1).any():
                raise KeyError("One or more row labels was not found")
            if (cidx == -1).any():
                raise KeyError("One or more column labels was not found")
            flat_index = ridx * len(self.columns) + cidx
            result = values.flat[flat_index]
        else:
            result = np.empty(n, dtype="O")
            for i, (r, c) in enumerate(zip(row_labels, col_labels)):
                result[i] = self._get_value(r, c)

        if is_object_dtype(result):
            result = lib.maybe_convert_objects(result)

        return result
