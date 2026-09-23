    def to_native_types(self, slicer=None, na_rep=None, date_format=None,
                        **kwargs):
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

        if date_format is None:
            date_formatter = lambda x: Timestamp(x)._repr_base
        else:
            date_formatter = lambda x: Timestamp(x).strftime(date_format)

        rvalues.flat[imask] = np.array([date_formatter(val) for val in
                                        values.ravel()[imask]], dtype=object)

        return rvalues.tolist()
