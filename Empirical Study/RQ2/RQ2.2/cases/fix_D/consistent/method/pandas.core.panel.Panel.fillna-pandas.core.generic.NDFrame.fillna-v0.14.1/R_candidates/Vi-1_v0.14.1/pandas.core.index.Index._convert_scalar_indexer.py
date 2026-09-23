    def _convert_scalar_indexer(self, key, typ=None):
        """ convert a scalar indexer, right now we are converting
        floats -> ints if the index supports it
        """

        def to_int():
            ikey = int(key)
            if ikey != key:
                return self._convert_indexer_error(key, 'label')
            return ikey

        if typ == 'iloc':
            if is_integer(key):
                return key
            elif is_float(key):
                key = to_int()
                warnings.warn("scalar indexers for index type {0} should be integers and not floating point".format(
                    type(self).__name__),FutureWarning)
                return key
            return self._convert_indexer_error(key, 'label')

        if is_float(key):
            if not self.is_floating():
                warnings.warn("scalar indexers for index type {0} should be integers and not floating point".format(
                    type(self).__name__),FutureWarning)
            return to_int()

        return key
