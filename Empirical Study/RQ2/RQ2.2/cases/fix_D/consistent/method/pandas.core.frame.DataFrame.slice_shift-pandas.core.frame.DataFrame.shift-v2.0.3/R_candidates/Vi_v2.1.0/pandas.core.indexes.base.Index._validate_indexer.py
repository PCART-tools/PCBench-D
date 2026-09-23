    @final
    def _validate_indexer(
        self,
        form: Literal["positional", "slice"],
        key,
        kind: Literal["getitem", "iloc"],
    ) -> None:
        """
        If we are positional indexer, validate that we have appropriate
        typed bounds must be an integer.
        """
        if not lib.is_int_or_none(key):
            self._raise_invalid_indexer(form, key)
