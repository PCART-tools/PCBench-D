    def _get_values_tuple(self, key):
        # mpl hackaround
        if com.any_none(*key):
            result = self._get_values(key)
            deprecate_ndim_indexing(result, stacklevel=find_stack_level())
            return result

        if not isinstance(self.index, MultiIndex):
            raise KeyError("key of type tuple not found and not a MultiIndex")

        # If key is contained, would have returned by now
        indexer, new_index = self.index.get_loc_level(key)
        return self._constructor(self._values[indexer], index=new_index).__finalize__(
            self
        )
