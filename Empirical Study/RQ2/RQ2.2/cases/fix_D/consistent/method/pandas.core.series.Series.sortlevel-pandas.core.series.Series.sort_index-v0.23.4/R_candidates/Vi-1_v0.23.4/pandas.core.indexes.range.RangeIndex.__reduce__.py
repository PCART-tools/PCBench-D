    def __reduce__(self):
        d = self._get_attributes_dict()
        d.update(dict(self._get_data_as_items()))
        return ibase._new_Index, (self.__class__, d), None
