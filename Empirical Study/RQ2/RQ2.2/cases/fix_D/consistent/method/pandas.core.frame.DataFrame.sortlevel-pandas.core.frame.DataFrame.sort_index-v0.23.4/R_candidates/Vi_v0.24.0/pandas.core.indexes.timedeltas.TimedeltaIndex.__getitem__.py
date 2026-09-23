    def __getitem__(self, key):
        result = self._data.__getitem__(key)
        if is_scalar(result):
            return result
        return type(self)(result, name=self.name)
