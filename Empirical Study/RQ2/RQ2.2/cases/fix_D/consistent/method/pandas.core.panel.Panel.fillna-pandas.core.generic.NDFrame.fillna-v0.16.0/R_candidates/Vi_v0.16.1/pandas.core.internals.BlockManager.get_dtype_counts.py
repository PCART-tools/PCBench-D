    def get_dtype_counts(self):
        return self._get_counts(lambda b: b.dtype.name)
