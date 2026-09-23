    @property
    def dtypes(self):
        return self.apply(lambda x: x.dtype, reduce=False)
