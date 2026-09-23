    def _set_with_engine(self, key, value):
        values = self._values
        if is_extension_array_dtype(values.dtype):
            # The cython indexing engine does not support ExtensionArrays.
            values[self.index.get_loc(key)] = value
            return
        try:
            self.index._engine.set_value(values, key, value)
            return
        except KeyError:
            values[self.index.get_loc(key)] = value
            return
