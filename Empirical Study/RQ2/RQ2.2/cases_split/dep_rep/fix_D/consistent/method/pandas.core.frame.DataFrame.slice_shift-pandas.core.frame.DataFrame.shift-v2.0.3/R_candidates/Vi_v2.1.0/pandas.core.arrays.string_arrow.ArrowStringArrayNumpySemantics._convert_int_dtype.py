    def _convert_int_dtype(self, result):
        if result.dtype == np.int32:
            result = result.astype(np.int64)
        return result
