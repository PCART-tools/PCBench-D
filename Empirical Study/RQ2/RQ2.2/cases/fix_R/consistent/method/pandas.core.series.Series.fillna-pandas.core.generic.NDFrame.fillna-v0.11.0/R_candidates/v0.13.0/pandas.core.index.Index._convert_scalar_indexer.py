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
            if not (is_integer(key) or is_float(key)):
                self._convert_indexer_error(key, 'label')
            return to_int()

        if is_float(key):
            return to_int()

        return key
