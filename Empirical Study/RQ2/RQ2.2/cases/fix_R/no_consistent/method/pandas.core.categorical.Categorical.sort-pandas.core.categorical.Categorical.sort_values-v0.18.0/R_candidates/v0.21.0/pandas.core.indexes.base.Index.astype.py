    @Appender(_index_shared_docs['astype'])
    def astype(self, dtype, copy=True):
        return Index(self.values.astype(dtype, copy=copy), name=self.name,
                     dtype=dtype)
