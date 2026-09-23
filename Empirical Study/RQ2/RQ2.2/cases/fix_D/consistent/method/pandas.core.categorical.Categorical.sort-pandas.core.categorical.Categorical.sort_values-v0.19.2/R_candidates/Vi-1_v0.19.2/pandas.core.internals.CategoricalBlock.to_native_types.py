    def to_native_types(self, slicer=None, na_rep='', quoting=None, **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            # Categorical is always one dimension
            values = values[slicer]
        mask = isnull(values)
        values = np.array(values, dtype='object')
        values[mask] = na_rep

        # we are expected to return a 2-d ndarray
        return values.reshape(1, len(values))
