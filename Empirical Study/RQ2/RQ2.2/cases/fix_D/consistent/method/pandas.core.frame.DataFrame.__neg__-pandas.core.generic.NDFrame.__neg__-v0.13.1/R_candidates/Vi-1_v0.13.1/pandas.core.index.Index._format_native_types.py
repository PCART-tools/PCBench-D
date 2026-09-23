    def _format_native_types(self, na_rep='', **kwargs):
        """ actually format my specific types """
        mask = isnull(self)
        values = np.array(self, dtype=object, copy=True)
        values[mask] = na_rep
        return values.tolist()
