    def __setstate__(self, data_dict):
        self.__dict__ = data_dict
        # turn the normal dictionary back into a dictionary with weak values
        # The extra lambda is to provide a callback to remove dead
        # weakrefs from the dictionary when garbage collection is done.
        self._parents = {
            k: weakref.ref(v, lambda _, pop=self._parents.pop, k=k: pop(k))
            for k, v in self._parents.items() if v is not None}
