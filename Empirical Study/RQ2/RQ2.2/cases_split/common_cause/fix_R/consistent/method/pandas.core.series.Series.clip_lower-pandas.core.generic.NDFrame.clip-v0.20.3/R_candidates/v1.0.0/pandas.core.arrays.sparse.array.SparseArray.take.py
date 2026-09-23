    def take(self, indices, allow_fill=False, fill_value=None):
        if is_scalar(indices):
            raise ValueError(f"'indices' must be an array, not a scalar '{indices}'.")
        indices = np.asarray(indices, dtype=np.int32)

        if indices.size == 0:
            result = []
            kwargs = {"dtype": self.dtype}
        elif allow_fill:
            result = self._take_with_fill(indices, fill_value=fill_value)
            kwargs = {}
        else:
            result = self._take_without_fill(indices)
            kwargs = {"dtype": self.dtype}

        return type(self)(result, fill_value=self.fill_value, kind=self.kind, **kwargs)
