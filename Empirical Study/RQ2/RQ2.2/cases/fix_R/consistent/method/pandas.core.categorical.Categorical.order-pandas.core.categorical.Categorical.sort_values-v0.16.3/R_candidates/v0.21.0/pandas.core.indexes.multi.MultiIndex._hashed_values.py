    @cache_readonly
    def _hashed_values(self):
        """ return a uint64 ndarray of my hashed values """
        from pandas.core.util.hashing import hash_tuples
        return hash_tuples(self)
