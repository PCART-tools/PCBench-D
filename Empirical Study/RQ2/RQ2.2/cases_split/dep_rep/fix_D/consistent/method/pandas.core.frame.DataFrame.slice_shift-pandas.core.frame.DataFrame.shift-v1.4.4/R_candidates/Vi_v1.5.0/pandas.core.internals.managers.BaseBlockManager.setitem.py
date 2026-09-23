    def setitem(self: T, indexer, value) -> T:
        """
        Set values with indexer.

        For SingleBlockManager, this backs s[indexer] = value
        """
        if isinstance(indexer, np.ndarray) and indexer.ndim > self.ndim:
            raise ValueError(f"Cannot set values with ndim > {self.ndim}")

        if _using_copy_on_write() and not self._has_no_reference(0):
            # if being referenced -> perform Copy-on-Write and clear the reference
            # this method is only called if there is a single block -> hardcoded 0
            self = self.copy()

        return self.apply("setitem", indexer=indexer, value=value)
