    def _mode(self: ArrowExtensionArrayT, dropna: bool = True) -> ArrowExtensionArrayT:
        """
        Returns the mode(s) of the ExtensionArray.

        Always returns `ExtensionArray` even if only one value.

        Parameters
        ----------
        dropna : bool, default True
            Don't consider counts of NA values.
            Not implemented by pyarrow.

        Returns
        -------
        same type as self
            Sorted, if possible.
        """
        if pa_version_under6p0:
            raise NotImplementedError("mode only supported for pyarrow version >= 6.0")
        modes = pc.mode(self._data, pc.count_distinct(self._data).as_py())
        values = modes.field(0)
        counts = modes.field(1)
        # counts sorted descending i.e counts[0] = max
        mask = pc.equal(counts, counts[0])
        most_common = values.filter(mask)
        return type(self)(most_common)
