    def _iter_column_arrays(self) -> Iterator[ArrayLike]:
        """
        Iterate over the arrays of all columns in order.
        This returns the values as stored in the Block (ndarray or ExtensionArray).
        """
        for i in range(len(self.columns)):
            yield self._get_column_array(i)
