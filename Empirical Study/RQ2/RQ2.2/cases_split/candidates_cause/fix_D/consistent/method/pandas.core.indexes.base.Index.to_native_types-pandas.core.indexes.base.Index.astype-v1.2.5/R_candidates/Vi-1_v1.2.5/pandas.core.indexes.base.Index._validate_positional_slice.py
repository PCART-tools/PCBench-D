    @final
    def _validate_positional_slice(self, key: slice):
        """
        For positional indexing, a slice must have either int or None
        for each of start, stop, and step.
        """
        self._validate_indexer("positional", key.start, "iloc")
        self._validate_indexer("positional", key.stop, "iloc")
        self._validate_indexer("positional", key.step, "iloc")
