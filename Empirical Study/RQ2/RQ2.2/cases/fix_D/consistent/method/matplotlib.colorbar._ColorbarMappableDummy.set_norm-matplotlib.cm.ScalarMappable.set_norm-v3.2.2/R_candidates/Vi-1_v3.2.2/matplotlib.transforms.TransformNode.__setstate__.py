    def __setstate__(self, data_dict):
        self.__dict__ = data_dict
        # turn the normal dictionary back into a dictionary with weak values
        # The extra lambda is to provide a callback to remove dead
        # weakrefs from the dictionary when garbage collection is done.
        self._parents = {k: weakref.ref(v, lambda ref, sid=k,
                                                  target=self._parents:
                                                        target.pop(sid))
                         for k, v in self._parents.items() if v is not None}
