    def _get_string_slice(self, key):
        if is_integer(key) or is_float(key) or key is NaT:
            self._invalid_indexer('slice', key)
        loc = self._partial_td_slice(key)
        return loc
