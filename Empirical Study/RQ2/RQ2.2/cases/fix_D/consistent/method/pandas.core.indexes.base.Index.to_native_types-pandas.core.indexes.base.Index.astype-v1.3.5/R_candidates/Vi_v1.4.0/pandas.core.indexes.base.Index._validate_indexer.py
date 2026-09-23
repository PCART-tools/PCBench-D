    @final
    def _validate_indexer(self, form: str_t, key, kind: str_t):
        """
        If we are positional indexer, validate that we have appropriate
        typed bounds must be an integer.
        """
        assert kind in ["getitem", "iloc"]

        if key is not None and not is_integer(key):
            raise self._invalid_indexer(form, key)
