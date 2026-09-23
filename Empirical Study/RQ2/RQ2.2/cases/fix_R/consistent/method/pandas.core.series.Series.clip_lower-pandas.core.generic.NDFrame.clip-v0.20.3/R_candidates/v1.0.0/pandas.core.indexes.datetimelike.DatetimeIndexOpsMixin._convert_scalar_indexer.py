    def _convert_scalar_indexer(self, key, kind=None):
        """
        We don't allow integer or float indexing on datetime-like when using
        loc.

        Parameters
        ----------
        key : label of the slice bound
        kind : {'ix', 'loc', 'getitem', 'iloc'} or None
        """

        assert kind in ["ix", "loc", "getitem", "iloc", None]

        # we don't allow integer/float indexing for loc
        # we don't allow float indexing for ix/getitem
        if is_scalar(key):
            is_int = is_integer(key)
            is_flt = is_float(key)
            if kind in ["loc"] and (is_int or is_flt):
                self._invalid_indexer("index", key)
            elif kind in ["ix", "getitem"] and is_flt:
                self._invalid_indexer("index", key)

        return super()._convert_scalar_indexer(key, kind=kind)
