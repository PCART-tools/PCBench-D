    def _convert_slice_indexer_getitem(self, key, is_index_slice=False):
        """ called from the getitem slicers, determine how to treat the key
            whether positional or not """
        if self.is_integer() or is_index_slice:
            return key
        return self._convert_slice_indexer(key)
