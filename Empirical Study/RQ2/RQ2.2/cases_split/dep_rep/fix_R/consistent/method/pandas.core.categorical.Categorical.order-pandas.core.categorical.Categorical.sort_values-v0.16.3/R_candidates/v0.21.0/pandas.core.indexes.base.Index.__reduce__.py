    def __reduce__(self):
        d = dict(data=self._data)
        d.update(self._get_attributes_dict())
        return _new_Index, (self.__class__, d), None
