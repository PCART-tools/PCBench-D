    def __setstate__(self, data_dict):
        self.__dict__ = data_dict
        # turn the normal dictionary back into a dictionary with weak
        # values
        self._parents = dict((k, weakref.ref(v)) for (k, v) in
                             six.iteritems(self._parents) if v is not None)
