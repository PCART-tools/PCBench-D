    def __reduce__(self):
        d = {"data": self._data, "name": self.name}
        return _new_Index, (type(self), d), None
