    @property
    def shape(self):
        # Avoid materializing self._values
        return self._ndarray_values.shape
