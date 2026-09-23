    def to_native_types(self, slicer=None, na_rep='', **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            # Categorical is always one dimension
            values = values[slicer]
        values = np.array(values, dtype=object)
        mask = isnull(values)
        values[mask] = na_rep
        # Blocks.to_native_type returns list of lists, but we are always only a list
        return [values.tolist()]
