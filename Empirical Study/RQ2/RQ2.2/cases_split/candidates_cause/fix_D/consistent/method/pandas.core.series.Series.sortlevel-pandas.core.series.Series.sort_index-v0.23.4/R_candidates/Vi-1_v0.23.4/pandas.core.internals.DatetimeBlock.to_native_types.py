    def to_native_types(self, slicer=None, na_rep=None, date_format=None,
                        quoting=None, **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            values = values[..., slicer]

        from pandas.io.formats.format import _get_format_datetime64_from_values
        format = _get_format_datetime64_from_values(values, date_format)

        result = tslib.format_array_from_datetime(
            values.view('i8').ravel(), tz=getattr(self.values, 'tz', None),
            format=format, na_rep=na_rep).reshape(values.shape)
        return np.atleast_2d(result)
