    def _set_with(self, key, value):
        # other: fancy integer or otherwise
        assert not isinstance(key, tuple)

        if is_scalar(key):
            key = [key]
        elif is_iterator(key):
            # Without this, the call to infer_dtype will consume the generator
            key = list(key)

        key_type = lib.infer_dtype(key, skipna=False)

        # Note: key_type == "boolean" should not occur because that
        #  should be caught by the is_bool_indexer check in __setitem__
        if key_type == "integer":
            if not self.index._should_fallback_to_positional:
                self._set_labels(key, value)
            else:
                self._set_values(key, value)
        else:
            self.loc[key] = value
