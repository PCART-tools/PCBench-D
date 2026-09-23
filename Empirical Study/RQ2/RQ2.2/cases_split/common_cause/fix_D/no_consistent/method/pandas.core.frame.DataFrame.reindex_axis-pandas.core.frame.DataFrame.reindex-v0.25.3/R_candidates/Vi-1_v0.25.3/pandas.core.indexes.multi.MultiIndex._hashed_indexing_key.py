    def _hashed_indexing_key(self, key):
        """
        validate and return the hash for the provided key

        *this is internal for use for the cython routines*

        Parameters
        ----------
        key : string or tuple

        Returns
        -------
        np.uint64

        Notes
        -----
        we need to stringify if we have mixed levels

        """
        from pandas.core.util.hashing import hash_tuples, hash_tuple

        if not isinstance(key, tuple):
            return hash_tuples(key)

        if not len(key) == self.nlevels:
            raise KeyError

        def f(k, stringify):
            if stringify and not isinstance(k, str):
                k = str(k)
            return k

        key = tuple(
            f(k, stringify) for k, stringify in zip(key, self._have_mixed_levels)
        )
        return hash_tuple(key)
