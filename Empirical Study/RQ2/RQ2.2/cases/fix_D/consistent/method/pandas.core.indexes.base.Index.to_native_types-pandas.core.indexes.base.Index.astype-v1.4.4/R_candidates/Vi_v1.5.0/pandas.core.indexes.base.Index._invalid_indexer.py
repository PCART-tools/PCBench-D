    @final
    def _invalid_indexer(self, form: str_t, key) -> TypeError:
        """
        Consistent invalid indexer message.
        """
        return TypeError(
            f"cannot do {form} indexing on {type(self).__name__} with these "
            f"indexers [{key}] of type {type(key).__name__}"
        )
