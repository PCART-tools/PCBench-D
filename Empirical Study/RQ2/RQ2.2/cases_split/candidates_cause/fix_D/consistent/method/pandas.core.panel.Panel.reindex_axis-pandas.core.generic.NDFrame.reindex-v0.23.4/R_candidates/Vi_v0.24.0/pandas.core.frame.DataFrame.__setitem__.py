    def __setitem__(self, key, value):
        key = com.apply_if_callable(key, self)

        # see if we can slice the rows
        indexer = convert_to_index_sliceable(self, key)
        if indexer is not None:
            return self._setitem_slice(indexer, value)

        if isinstance(key, DataFrame) or getattr(key, 'ndim', None) == 2:
            self._setitem_frame(key, value)
        elif isinstance(key, (Series, np.ndarray, list, Index)):
            self._setitem_array(key, value)
        else:
            # set column
            self._set_item(key, value)
