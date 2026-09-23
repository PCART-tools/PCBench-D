    def __setstate__(self, data_dict):
        self.__dict__ = data_dict
        # turn the normal dictionary back into a dictionary with weak values
        self._parents = {k: weakref.ref(v)
                         for k, v in self._parents.items() if v is not None}
