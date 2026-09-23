    @cache_readonly
    def inferred_type(self) -> str_t:
        """
        Return a string of the type inferred from the values.

        Examples
        --------
        >>> idx = pd.Index([1, 2, 3])
        >>> idx
        Index([1, 2, 3], dtype='int64')
        >>> idx.inferred_type
        'integer'
        """
        return lib.infer_dtype(self._values, skipna=False)
