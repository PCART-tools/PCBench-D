    def __setitem__(self, key, value):

        # see if we can slice the rows
        indexer = _convert_to_index_sliceable(self, key)
        if indexer is not None:
            return self._setitem_slice(indexer, value)

        if isinstance(key, (Series, np.ndarray, list, Index)):
            self._setitem_array(key, value)
        elif isinstance(key, DataFrame):
            self._setitem_frame(key, value)
        else:
            # set column
            self._set_item(key, value)
