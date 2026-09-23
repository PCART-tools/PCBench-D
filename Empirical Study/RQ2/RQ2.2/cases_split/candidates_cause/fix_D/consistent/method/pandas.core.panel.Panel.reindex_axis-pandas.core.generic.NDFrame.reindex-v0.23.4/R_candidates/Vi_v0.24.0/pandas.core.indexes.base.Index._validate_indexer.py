    def _validate_indexer(self, form, key, kind):
        """
        If we are positional indexer, validate that we have appropriate
        typed bounds must be an integer.
        """
        assert kind in ['ix', 'loc', 'getitem', 'iloc']

        if key is None:
            pass
        elif is_integer(key):
            pass
        elif kind in ['iloc', 'getitem']:
            self._invalid_indexer(form, key)
        return key
