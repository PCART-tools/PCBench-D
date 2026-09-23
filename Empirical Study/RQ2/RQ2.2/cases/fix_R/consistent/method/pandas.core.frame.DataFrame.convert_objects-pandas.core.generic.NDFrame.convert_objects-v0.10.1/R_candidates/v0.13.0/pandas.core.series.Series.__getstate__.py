    def __getstate__(self):
        return dict(_data=self._data, name=self.name)
