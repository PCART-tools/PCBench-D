    def _validate_key(self, key, axis):
        if com.is_bool_indexer(key):
            if hasattr(key, 'index') and isinstance(key.index, Index):
                if key.index.inferred_type == 'integer':
                    raise NotImplementedError("iLocation based boolean "
                                              "indexing on an integer type "
                                              "is not available")
                raise ValueError("iLocation based boolean indexing cannot use "
                                 "an indexable as a mask")
            return

        if isinstance(key, slice):
            return
        elif is_integer(key):
            self._validate_integer(key, axis)
        elif isinstance(key, tuple):
            # a tuple should already have been caught by this point
            # so don't treat a tuple as a valid indexer
            raise IndexingError('Too many indexers')
        elif is_list_like_indexer(key):
            # check that the key does not exceed the maximum size of the index
            arr = np.array(key)
            len_axis = len(self.obj._get_axis(axis))

            if len(arr) and (arr.max() >= len_axis or arr.min() < -len_axis):
                raise IndexError("positional indexers are out-of-bounds")
        else:
            raise ValueError("Can only index by location with "
                             "a [{types}]".format(types=self._valid_types))
