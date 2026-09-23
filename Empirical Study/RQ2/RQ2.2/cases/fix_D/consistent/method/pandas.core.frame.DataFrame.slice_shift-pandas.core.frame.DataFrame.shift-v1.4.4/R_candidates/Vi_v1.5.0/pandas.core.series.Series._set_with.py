    def _set_with(self, key, value):
        # We got here via exception-handling off of InvalidIndexError, so
        #  key should always be listlike at this point.
        assert not isinstance(key, tuple)

        if is_iterator(key):
            # Without this, the call to infer_dtype will consume the generator
            key = list(key)

        if not self.index._should_fallback_to_positional:
            # Regardless of the key type, we're treating it as labels
            self._set_labels(key, value)

        else:
            # Note: key_type == "boolean" should not occur because that
            #  should be caught by the is_bool_indexer check in __setitem__
            key_type = lib.infer_dtype(key, skipna=False)

            if key_type == "integer":
                self._set_values(key, value)
            else:
                self._set_labels(key, value)
