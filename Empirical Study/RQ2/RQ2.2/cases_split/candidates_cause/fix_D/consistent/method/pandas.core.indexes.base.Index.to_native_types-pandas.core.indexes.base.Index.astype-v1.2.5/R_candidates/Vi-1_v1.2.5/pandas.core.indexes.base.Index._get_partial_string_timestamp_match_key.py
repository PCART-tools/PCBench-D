    def _get_partial_string_timestamp_match_key(self, key):
        """
        Translate any partial string timestamp matches in key, returning the
        new key.

        Only relevant for MultiIndex.
        """
        # GH#10331
        return key
