    @cache_readonly
    def inferred_type(self) -> str_t:
        """
        Return a string of the type inferred from the values.
        """
        return lib.infer_dtype(self._values, skipna=False)
