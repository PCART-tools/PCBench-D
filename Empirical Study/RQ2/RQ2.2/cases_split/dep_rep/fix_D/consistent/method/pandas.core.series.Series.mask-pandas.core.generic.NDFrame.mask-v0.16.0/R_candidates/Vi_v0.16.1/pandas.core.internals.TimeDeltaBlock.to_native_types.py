    def to_native_types(self, slicer=None, na_rep=None, quoting=None, **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            values = values[:, slicer]
        mask = isnull(values)

        rvalues = np.empty(values.shape, dtype=object)
        if na_rep is None:
            na_rep = 'NaT'
        rvalues[mask] = na_rep
        imask = (~mask).ravel()

        #### FIXME ####
        # should use the core.format.Timedelta64Formatter here
        # to figure what format to pass to the Timedelta
        # e.g. to not show the decimals say
        rvalues.flat[imask] = np.array([Timedelta(val)._repr_base(format='all')
                                        for val in values.ravel()[imask]],
                                       dtype=object)
        return rvalues
