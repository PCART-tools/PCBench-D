    def _has_valid_tuple(self, key: Tuple):
        """
        Check the key for valid keys across my indexer.
        """
        for i, k in enumerate(key):
            if i >= self.ndim:
                raise IndexingError("Too many indexers")
            try:
                self._validate_key(k, i)
            except ValueError:
                raise ValueError(
                    "Location based indexing can only have "
                    f"[{self._valid_types}] types"
                )
