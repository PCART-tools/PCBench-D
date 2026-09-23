    @cache_readonly
    def _hashed_values(self):
        """ return a uint64 ndarray of my hashed values """
        return hash_tuples(self)
