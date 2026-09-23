    @doc(ExtensionArray.shift)
    def shift(self, periods: int = 1, fill_value=None, axis: AxisInt = 0):
        fill_value = self._validate_scalar(fill_value)
        new_values = shift(self._ndarray, periods, axis, fill_value)

        return self._from_backing_data(new_values)
