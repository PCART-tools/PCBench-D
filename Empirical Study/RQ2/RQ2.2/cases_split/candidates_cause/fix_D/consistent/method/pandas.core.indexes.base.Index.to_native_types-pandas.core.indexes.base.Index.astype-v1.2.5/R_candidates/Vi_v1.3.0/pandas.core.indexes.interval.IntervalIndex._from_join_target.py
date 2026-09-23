    def _from_join_target(self, result):
        left, right = list(zip(*result))
        arr = type(self._data).from_arrays(
            left, right, dtype=self.dtype, closed=self.closed
        )
        return type(self)._simple_new(arr, name=self.name)
