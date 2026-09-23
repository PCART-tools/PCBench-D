    @final
    def _validate_indexer(self, form: str_t, key, kind: str_t):
        """
        If we are positional indexer, validate that we have appropriate
        typed bounds must be an integer.
        """
        assert kind in ["getitem", "iloc"]

        if key is None:
            pass
        elif is_integer(key):
            pass
        else:
            raise self._invalid_indexer(form, key)
