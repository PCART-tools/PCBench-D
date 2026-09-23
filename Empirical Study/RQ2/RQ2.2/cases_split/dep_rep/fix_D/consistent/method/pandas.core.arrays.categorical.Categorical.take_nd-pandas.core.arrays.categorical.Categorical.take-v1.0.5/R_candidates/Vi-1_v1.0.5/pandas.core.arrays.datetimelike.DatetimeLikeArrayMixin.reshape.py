    def reshape(self, *args, **kwargs):
        # Note: we drop any freq
        data = self._data.reshape(*args, **kwargs)
        return type(self)(data, dtype=self.dtype)
