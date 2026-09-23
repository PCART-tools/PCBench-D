    def _invalid_indexer(self, form, key):
        """
        Consistent invalid indexer message.
        """
        raise TypeError(
            f"cannot do {form} indexing on {type(self)} with these "
            f"indexers [{key}] of {type(key)}"
        )
