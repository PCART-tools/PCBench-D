    def to_native_types(self, slicer=None, na_rep=None, **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            values = values[:, slicer]
        mask = isnull(values)

        rvalues = np.empty(values.shape, dtype=object)
        if na_rep is None:
            na_rep = 'NaT'
        rvalues[mask] = na_rep
        imask = (-mask).ravel()
        rvalues.flat[imask] = np.array([lib.repr_timedelta64(val)
                                        for val in values.ravel()[imask]],
                                       dtype=object)
        return rvalues.tolist()
