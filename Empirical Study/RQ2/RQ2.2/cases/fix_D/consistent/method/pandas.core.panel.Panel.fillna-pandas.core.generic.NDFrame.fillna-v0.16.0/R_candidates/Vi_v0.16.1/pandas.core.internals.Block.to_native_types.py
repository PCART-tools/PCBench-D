    def to_native_types(self, slicer=None, na_rep='', quoting=None, **kwargs):
        """ convert to our native types format, slicing if desired """

        values = self.values
        if slicer is not None:
            values = values[:, slicer]
        mask = isnull(values)

        if not self.is_object and not quoting:
            values = values.astype(str)
        else:
            values = np.array(values, dtype='object')

        values[mask] = na_rep
        return values
