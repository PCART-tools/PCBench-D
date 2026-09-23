    def __reduce__(self):
        d = {"data": self._data, "name": self.name}
        return _new_DatetimeIndex, (type(self), d), None
