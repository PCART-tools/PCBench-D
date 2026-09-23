    def _get_partial_string_timestamp_match_key(self, key):
        """
        Translate any partial string timestamp matches in key, returning the
        new key.

        Only relevant for MultiIndex.
        """
        # GH#10331
        if isinstance(key, str) and self.levels[0]._supports_partial_string_indexing:
            # Convert key '2016-01-01' to
            # ('2016-01-01'[, slice(None, None, None)]+)
            key = (key,) + (slice(None),) * (len(self.levels) - 1)

        if isinstance(key, tuple):
            # Convert (..., '2016-01-01', ...) in tuple to
            # (..., slice('2016-01-01', '2016-01-01', None), ...)
            new_key = []
            for i, component in enumerate(key):
                if (
                    isinstance(component, str)
                    and self.levels[i]._supports_partial_string_indexing
                ):
                    new_key.append(slice(component, component, None))
                else:
                    new_key.append(component)
            key = tuple(new_key)

        return key
