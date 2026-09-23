    def __getitem__(self, key):
        """
        This getitem defers to the underlying array, which by-definition can
        only handle list-likes, slices, and integer scalars
        """

        is_int = lib.is_integer(key)
        if lib.is_scalar(key) and not is_int:
            raise IndexError(
                "only integers, slices (`:`), ellipsis (`...`), "
                "numpy.newaxis (`None`) and integer or boolean "
                "arrays are valid indices"
            )

        getitem = self._data.__getitem__
        if is_int:
            val = getitem(key)
            if lib.is_scalar(val):
                # i.e. self.ndim == 1
                return self._box_func(val)
            return type(self)(val, dtype=self.dtype)

        if com.is_bool_indexer(key):
            # first convert to boolean, because check_array_indexer doesn't
            # allow object dtype
            key = np.asarray(key, dtype=bool)
            key = check_array_indexer(self, key)
            if key.all():
                key = slice(0, None, None)
            else:
                key = lib.maybe_booleans_to_slice(key.view(np.uint8))
        elif isinstance(key, list) and len(key) == 1 and isinstance(key[0], slice):
            # see https://github.com/pandas-dev/pandas/issues/31299, need to allow
            # this for now (would otherwise raise in check_array_indexer)
            pass
        else:
            key = check_array_indexer(self, key)

        is_period = is_period_dtype(self)
        if is_period:
            freq = self.freq
        else:
            freq = None
            if isinstance(key, slice):
                if self.freq is not None and key.step is not None:
                    freq = key.step * self.freq
                else:
                    freq = self.freq
            elif key is Ellipsis:
                # GH#21282 indexing with Ellipsis is similar to a full slice,
                #  should preserve `freq` attribute
                freq = self.freq

        result = getitem(key)
        if result.ndim > 1:
            # To support MPL which performs slicing with 2 dim
            # even though it only has 1 dim by definition
            return result

        return self._simple_new(result, dtype=self.dtype, freq=freq)
