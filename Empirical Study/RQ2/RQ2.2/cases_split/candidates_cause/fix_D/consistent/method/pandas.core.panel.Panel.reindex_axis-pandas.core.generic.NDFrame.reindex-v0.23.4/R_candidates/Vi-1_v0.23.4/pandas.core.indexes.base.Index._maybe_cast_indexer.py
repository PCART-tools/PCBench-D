    def _maybe_cast_indexer(self, key):
        """
        If we have a float key and are not a floating index
        then try to cast to an int if equivalent
        """

        if is_float(key) and not self.is_floating():
            try:
                ckey = int(key)
                if ckey == key:
                    key = ckey
            except (OverflowError, ValueError, TypeError):
                pass
        return key
