    def _try_coerce_and_cast_result(self, result, dtype=None):
        result = self._try_coerce_result(result)
        result = self._try_cast_result(result, dtype=dtype)
        return result
