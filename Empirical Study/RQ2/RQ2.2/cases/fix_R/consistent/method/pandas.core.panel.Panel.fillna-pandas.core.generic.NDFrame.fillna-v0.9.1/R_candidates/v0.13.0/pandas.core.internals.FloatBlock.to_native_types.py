    def to_native_types(self, slicer=None, na_rep='', float_format=None,
                        **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            values = values[:, slicer]
        values = np.array(values, dtype=object)
        mask = isnull(values)
        values[mask] = na_rep
        if float_format:
            imask = (-mask).ravel()
            values.flat[imask] = np.array(
                [float_format % val for val in values.ravel()[imask]])
        return values.tolist()
