    def __getitem__(self, key):
        check_dict_or_set_indexers(key)
        key = com.apply_if_callable(key, self)

        if key is Ellipsis:
            return self

        key_is_scalar = is_scalar(key)
        if isinstance(key, (list, tuple)):
            key = unpack_1tuple(key)

        if is_integer(key) and self.index._should_fallback_to_positional:
            warnings.warn(
                # GH#50617
                "Series.__getitem__ treating keys as positions is deprecated. "
                "In a future version, integer keys will always be treated "
                "as labels (consistent with DataFrame behavior). To access "
                "a value by position, use `ser.iloc[pos]`",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            return self._values[key]

        elif key_is_scalar:
            return self._get_value(key)

        # Convert generator to list before going through hashable part
        # (We will iterate through the generator there to check for slices)
        if is_iterator(key):
            key = list(key)

        if is_hashable(key) and not isinstance(key, slice):
            # Otherwise index.get_value will raise InvalidIndexError
            try:
                # For labels that don't resolve as scalars like tuples and frozensets
                result = self._get_value(key)

                return result

            except (KeyError, TypeError, InvalidIndexError):
                # InvalidIndexError for e.g. generator
                #  see test_series_getitem_corner_generator
                if isinstance(key, tuple) and isinstance(self.index, MultiIndex):
                    # We still have the corner case where a tuple is a key
                    # in the first level of our MultiIndex
                    return self._get_values_tuple(key)

        if isinstance(key, slice):
            # Do slice check before somewhat-costly is_bool_indexer
            return self._getitem_slice(key)

        if com.is_bool_indexer(key):
            key = check_bool_indexer(self.index, key)
            key = np.asarray(key, dtype=bool)
            return self._get_rows_with_mask(key)

        return self._get_with(key)
