    def _maybe_cast_indexer(self, key):
        """
        If we have a float key and are not a floating index, then try to cast
        to an int if equivalent.
        """
        if not self.is_floating():
            return com.cast_scalar_indexer(key)
        return key
