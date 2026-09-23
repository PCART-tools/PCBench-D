    @cache_readonly
    def inferred_type(self):
        """
        Return a string of the type inferred from the values.
        """
        return lib.infer_dtype(self, skipna=False)
