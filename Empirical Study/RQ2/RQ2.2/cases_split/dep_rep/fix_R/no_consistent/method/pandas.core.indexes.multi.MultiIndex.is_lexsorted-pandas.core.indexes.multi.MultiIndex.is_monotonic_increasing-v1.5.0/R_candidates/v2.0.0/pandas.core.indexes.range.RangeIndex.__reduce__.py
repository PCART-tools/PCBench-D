    def __reduce__(self):
        d = {"name": self.name}
        d.update(dict(self._get_data_as_items()))
        return ibase._new_Index, (type(self), d), None
