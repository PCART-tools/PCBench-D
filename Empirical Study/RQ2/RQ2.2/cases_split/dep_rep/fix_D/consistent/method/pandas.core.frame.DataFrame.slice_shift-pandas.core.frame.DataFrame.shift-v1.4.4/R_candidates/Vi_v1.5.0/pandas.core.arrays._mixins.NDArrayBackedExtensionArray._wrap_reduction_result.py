    def _wrap_reduction_result(self, axis: int | None, result):
        if axis is None or self.ndim == 1:
            return self._box_func(result)
        return self._from_backing_data(result)
