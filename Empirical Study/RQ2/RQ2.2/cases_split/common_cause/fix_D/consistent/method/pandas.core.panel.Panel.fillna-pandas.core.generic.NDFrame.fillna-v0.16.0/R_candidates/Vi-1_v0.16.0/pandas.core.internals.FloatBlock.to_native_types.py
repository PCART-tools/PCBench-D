    def to_native_types(self, slicer=None, na_rep='', float_format=None, decimal='.',
                        **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            values = values[:, slicer]
        values = np.array(values, dtype=object)
        mask = isnull(values)
        values[mask] = na_rep


        if float_format and decimal != '.':
            formatter = lambda v : (float_format % v).replace('.',decimal,1)
        elif decimal != '.':
            formatter = lambda v : ('%g' % v).replace('.',decimal,1)
        elif float_format:
            formatter = lambda v : float_format % v
        else:
            formatter = None

        if formatter:
            imask = (~mask).ravel()
            values.flat[imask] = np.array(
                [formatter(val) for val in values.ravel()[imask]])

        return values.tolist()
