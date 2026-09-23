    def _getitem_axis(self, key, axis=0, validate_iterable=False):
        labels = self.obj._get_axis(axis)

        if isinstance(key, slice):
            self._has_valid_type(key, axis)
            return self._get_slice_axis(key, axis=axis)
        elif com._is_bool_indexer(key):
            return self._getbool_axis(key, axis=axis)
        elif _is_list_like(key) and not (isinstance(key, tuple) and
                                         isinstance(labels, MultiIndex)):

            if hasattr(key, 'ndim') and key.ndim > 1:
                raise ValueError('Cannot index with multidimensional key')

            if validate_iterable:
                self._has_valid_type(key, axis)
            return self._getitem_iterable(key, axis=axis)
        elif _is_nested_tuple(key, labels):
            locs = labels.get_locs(key)
            indexer = [ slice(None) ] * self.ndim
            indexer[axis] = locs
            return self.obj.iloc[tuple(indexer)]
        else:
            self._has_valid_type(key, axis)
            return self._get_label(key, axis=axis)
