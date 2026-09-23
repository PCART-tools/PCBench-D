    def _convert_scalar_indexer(self, key, kind=None):
        """
        convert a scalar indexer

        Parameters
        ----------
        key : label of the slice bound
        kind : optional, type of the indexing operation (loc/ix/iloc/None)

        right now we are converting
        floats -> ints if the index supports it
        """

        def to_int():
            ikey = int(key)
            if ikey != key:
                return self._invalid_indexer('label', key)
            return ikey

        if kind == 'iloc':
            if is_integer(key):
                return key
            elif is_float(key):
                key = to_int()
                warnings.warn("scalar indexers for index type {0} should be integers and not floating point".format(
                    type(self).__name__),FutureWarning)
                return key
            return self._invalid_indexer('label', key)

        if is_float(key):
            if not self.is_floating():
                warnings.warn("scalar indexers for index type {0} should be integers and not floating point".format(
                    type(self).__name__),FutureWarning)
            return to_int()

        return key
