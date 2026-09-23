    def take(self, indices, allow_fill=False, fill_value=None):
        if fill_value is None:
            # Primarily for subclasses
            fill_value = self.dtype.na_value
        result = take(
            self._ndarray, indices, allow_fill=allow_fill, fill_value=fill_value
        )
        return type(self)(result)
