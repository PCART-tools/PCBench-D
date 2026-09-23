    @Appender(_index_shared_docs["_shallow_copy"])
    def _shallow_copy(self, values=None, dtype=None, **kwargs):
        if dtype is None:
            dtype = self.dtype
        return super()._shallow_copy(values=values, dtype=dtype, **kwargs)
