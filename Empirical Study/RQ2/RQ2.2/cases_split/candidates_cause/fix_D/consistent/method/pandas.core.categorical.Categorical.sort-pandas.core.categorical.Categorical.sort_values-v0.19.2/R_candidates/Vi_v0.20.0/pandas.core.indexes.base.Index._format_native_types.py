    def _format_native_types(self, na_rep='', quoting=None, **kwargs):
        """ actually format my specific types """
        mask = isnull(self)
        if not self.is_object() and not quoting:
            values = np.asarray(self).astype(str)
        else:
            values = np.array(self, dtype=object, copy=True)

        values[mask] = na_rep
        return values
