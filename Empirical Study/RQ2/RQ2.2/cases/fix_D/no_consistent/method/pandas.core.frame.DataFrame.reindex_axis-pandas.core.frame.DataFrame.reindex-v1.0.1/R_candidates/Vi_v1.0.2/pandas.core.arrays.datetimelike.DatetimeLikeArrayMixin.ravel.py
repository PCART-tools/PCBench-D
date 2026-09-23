    def ravel(self, *args, **kwargs):
        # Note: we drop any freq
        data = self._data.ravel(*args, **kwargs)
        return type(self)(data, dtype=self.dtype)
