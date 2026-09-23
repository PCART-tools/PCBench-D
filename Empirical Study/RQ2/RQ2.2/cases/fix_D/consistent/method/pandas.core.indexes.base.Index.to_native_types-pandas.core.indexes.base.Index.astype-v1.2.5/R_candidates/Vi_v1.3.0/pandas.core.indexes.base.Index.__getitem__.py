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

        if is_scalar(key):
            key = com.cast_scalar_indexer(key, warn_float=True)
            return getitem(key)

        if isinstance(key, slice):
            # This case is separated from the conditional above to avoid
            # pessimization of basic indexing.
            result = getitem(key)
            # Going through simple_new for performance.
            return type(self)._simple_new(result, name=self._name)

        if com.is_bool_indexer(key):
            key = np.asarray(key, dtype=bool)

        result = getitem(key)
        if not is_scalar(result):
            # error: Argument 1 to "ndim" has incompatible type "Union[ExtensionArray,
            # Any]"; expected "Union[Union[int, float, complex, str, bytes, generic],
            # Sequence[Union[int, float, complex, str, bytes, generic]],
            # Sequence[Sequence[Any]], _SupportsArray]"
            if np.ndim(result) > 1:  # type: ignore[arg-type]
                deprecate_ndim_indexing(result)
                return result
            # NB: Using _constructor._simple_new would break if MultiIndex
            #  didn't override __getitem__
            return self._constructor._simple_new(result, name=self._name)
        else:
            return result
