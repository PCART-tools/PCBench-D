    @final
    def _raise_invalid_indexer(
        self,
        form: str_t,
        key,
        reraise: lib.NoDefault | None | Exception = lib.no_default,
    ) -> None:
        """
        Raise consistent invalid indexer message.
        """
        msg = (
            f"cannot do {form} indexing on {type(self).__name__} with these "
            f"indexers [{key}] of type {type(key).__name__}"
        )
        if reraise is not lib.no_default:
            raise TypeError(msg) from reraise
        raise TypeError(msg)
