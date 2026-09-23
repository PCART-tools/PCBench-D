    @final
    def _validate_tuple_indexer(self, key: tuple) -> tuple:
        """
        Check the key for valid keys across my indexer.
        """
        key = self._validate_key_length(key)
        key = self._expand_ellipsis(key)
        for i, k in enumerate(key):
            try:
                self._validate_key(k, i)
            except ValueError as err:
                raise ValueError(
                    "Location based indexing can only have "
                    f"[{self._valid_types}] types"
                ) from err
        return key
