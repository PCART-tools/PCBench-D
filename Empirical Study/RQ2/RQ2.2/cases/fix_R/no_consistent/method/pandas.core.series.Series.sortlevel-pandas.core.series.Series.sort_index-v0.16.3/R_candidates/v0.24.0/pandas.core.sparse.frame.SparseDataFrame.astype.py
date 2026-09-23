    def astype(self, dtype):
        return self._apply_columns(lambda x: x.astype(dtype))
