    @property
    def size(self):
        # Avoid materializing self._values
        return self._ndarray_values.size
