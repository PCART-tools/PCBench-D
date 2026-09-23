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
        __getitem__ = super(Index, self).__getitem__
        if np.isscalar(key):
            return __getitem__(key)

        if isinstance(key, slice):
            # This case is separated from the conditional above to avoid
            # pessimization of basic indexing.
            return __getitem__(key)

        if com._is_bool_indexer(key):
            return __getitem__(np.asarray(key))

        result = __getitem__(key)
        if result.ndim > 1:
            return result.view(np.ndarray)
        else:
            return result
