    def to_native_types(self, slicer=None, na_rep="nan", quoting=None, **kwargs):
        """override to use ExtensionArray astype for the conversion"""
        values = self.values
        if slicer is not None:
            values = values[slicer]
        mask = isna(values)

        values = np.asarray(values.astype(object))
        values[mask] = na_rep

        # we are expected to return a 2-d ndarray
        return values.reshape(1, len(values))
