    @Appender(ExtensionArray.shift.__doc__)
    def shift(self, periods=1, fill_value=None, axis=0):

        fill_value = self._validate_shift_value(fill_value)
        new_values = shift(self._data, periods, axis, fill_value)

        return type(self)._simple_new(new_values, dtype=self.dtype)
