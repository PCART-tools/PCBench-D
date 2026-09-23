    def _get_values_tuple(self, key):
        # mpl hackaround
        if _any_none(*key):
            return self._get_values(key)

        if not isinstance(self.index, MultiIndex):
            raise ValueError('Can only tuple-index with a MultiIndex')

        # If key is contained, would have returned by now
        indexer, new_index = self.index.get_loc_level(key)
        return self._constructor(self._values[indexer],
                                 index=new_index).__finalize__(self)
