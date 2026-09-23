    def to_native_types(self, slicer=None, na_rep='', float_format=None, decimal='.',
                        quoting=None, **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            values = values[:, slicer]
        mask = isnull(values)

        formatter = None
        if float_format and decimal != '.':
            formatter = lambda v : (float_format % v).replace('.',decimal,1)
        elif decimal != '.':
            formatter = lambda v : ('%g' % v).replace('.',decimal,1)
        elif float_format:
            formatter = lambda v : float_format % v

        if formatter is None and not quoting:
            values = values.astype(str)
        else:
            values = np.array(values, dtype='object')

        values[mask] = na_rep
        if formatter:
            imask = (~mask).ravel()
            values.flat[imask] = np.array(
                [formatter(val) for val in values.ravel()[imask]])

        return values
