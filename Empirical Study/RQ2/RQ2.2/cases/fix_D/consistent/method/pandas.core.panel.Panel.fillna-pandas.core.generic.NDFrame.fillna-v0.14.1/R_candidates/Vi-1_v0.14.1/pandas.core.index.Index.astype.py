    def astype(self, dtype):
        return Index(self.values.astype(dtype), name=self.name,
                     dtype=dtype)
