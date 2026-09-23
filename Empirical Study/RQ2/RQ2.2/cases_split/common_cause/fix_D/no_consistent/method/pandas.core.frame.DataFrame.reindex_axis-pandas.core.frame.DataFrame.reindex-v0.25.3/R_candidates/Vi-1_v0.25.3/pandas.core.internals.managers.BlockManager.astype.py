    def astype(self, dtype, **kwargs):
        return self.apply("astype", dtype=dtype, **kwargs)
