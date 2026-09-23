    def _convert_slice_indexer_iloc(self, key):
        """ convert a slice indexer for iloc only """
        self._validate_slicer(key, lambda v: v is None or is_integer(v))
        return key
