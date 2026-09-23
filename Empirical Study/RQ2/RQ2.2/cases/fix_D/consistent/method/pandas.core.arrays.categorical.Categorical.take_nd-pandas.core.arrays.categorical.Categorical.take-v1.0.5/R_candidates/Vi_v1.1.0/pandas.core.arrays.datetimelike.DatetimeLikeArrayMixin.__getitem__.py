    def __getitem__(self, key):
        """
        This getitem defers to the underlying array, which by-definition can
        only handle list-likes, slices, and integer scalars
        """

        if lib.is_integer(key):
            # fast-path
            result = self._data[key]
            if self.ndim == 1:
                return self._box_func(result)
            return self._simple_new(result, dtype=self.dtype)

        if com.is_bool_indexer(key):
            # first convert to boolean, because check_array_indexer doesn't
            # allow object dtype
            if is_object_dtype(key):
                key = np.asarray(key, dtype=bool)

            key = check_array_indexer(self, key)
            key = lib.maybe_booleans_to_slice(key.view(np.uint8))
        elif isinstance(key, list) and len(key) == 1 and isinstance(key[0], slice):
            # see https://github.com/pandas-dev/pandas/issues/31299, need to allow
            # this for now (would otherwise raise in check_array_indexer)
            pass
        else:
            key = check_array_indexer(self, key)

        freq = self._get_getitem_freq(key)
        result = self._data[key]
        if lib.is_scalar(result):
            return self._box_func(result)
        return self._simple_new(result, dtype=self.dtype, freq=freq)
