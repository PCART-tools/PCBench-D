    def to_native_types(self, slicer=None, na_rep="nan", quoting=None, **kwargs):
        """override to use ExtensionArray astype for the conversion"""
        values = self.values
        if slicer is not None:
            values = values[slicer]
        mask = isna(values)

        try:
            values = values.astype(str)
            values[mask] = na_rep
        except Exception:
            # eg SparseArray does not support setitem, needs to be converted to ndarray
            return super().to_native_types(slicer, na_rep, quoting, **kwargs)

        # we are expected to return a 2-d ndarray
        return values.reshape(1, len(values))
