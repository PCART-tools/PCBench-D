    @cache_readonly
    def inferred_type(self):
        """ return a string of the type inferred from the values """
        return lib.infer_dtype(self)
