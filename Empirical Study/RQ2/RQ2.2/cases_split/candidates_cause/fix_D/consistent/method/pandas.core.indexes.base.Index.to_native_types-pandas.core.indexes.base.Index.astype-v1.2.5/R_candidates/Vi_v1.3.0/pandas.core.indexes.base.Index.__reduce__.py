    def __reduce__(self):
        d = {"data": self._data}
        d.update(self._get_attributes_dict())
        return _new_Index, (type(self), d), None
