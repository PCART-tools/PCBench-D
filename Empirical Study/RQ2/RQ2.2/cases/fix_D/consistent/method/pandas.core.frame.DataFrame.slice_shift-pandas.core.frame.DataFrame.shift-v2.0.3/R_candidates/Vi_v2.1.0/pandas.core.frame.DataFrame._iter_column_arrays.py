    def _iter_column_arrays(self) -> Iterator[ArrayLike]:
        """
        Iterate over the arrays of all columns in order.
        This returns the values as stored in the Block (ndarray or ExtensionArray).

        Warning! The returned array is a view but doesn't handle Copy-on-Write,
        so this should be used with caution (for read-only purposes).
        """
        if isinstance(self._mgr, ArrayManager):
            yield from self._mgr.arrays
        else:
            for i in range(len(self.columns)):
                yield self._get_column_array(i)
