    @cache_readonly
    def inferred_type(self):
        return lib.infer_dtype(self)
