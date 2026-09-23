    @property
    def values(self):
        if self._tuples is not None:
            return self._tuples

        values = []

        for i in range(self.nlevels):
            vals = self._get_level_values(i)
            if is_categorical_dtype(vals):
                vals = vals.get_values()
            if (isinstance(vals.dtype, (PandasExtensionDtype, ExtensionDtype))
                    or hasattr(vals, '_box_values')):
                vals = vals.astype(object)
            vals = np.array(vals, copy=False)
            values.append(vals)

        self._tuples = lib.fast_zip(values)
        return self._tuples
