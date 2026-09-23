    def __getitem__(self, key):
        """
        Override numpy.ndarray's __getitem__ method to work as desired.

        This function adds lists and Series as valid boolean indexers
        (ndarrays only supports ndarray with dtype=bool).

        If resulting ndim != 1, plain ndarray is returned instead of
        corresponding `Index` subclass.

        """
        # There's no custom logic to be implemented in __getslice__, so it's
        # not overloaded intentionally.
        getitem = self._data.__getitem__
        promote = self._shallow_copy

        if np.isscalar(key):
            return getitem(key)

        if isinstance(key, slice):
            # This case is separated from the conditional above to avoid
            # pessimization of basic indexing.
            return promote(getitem(key))

        if com._is_bool_indexer(key):
            key = np.asarray(key)

        key = _values_from_object(key)
        result = getitem(key)
        if not np.isscalar(result):
            return promote(result)
        else:
            return result
