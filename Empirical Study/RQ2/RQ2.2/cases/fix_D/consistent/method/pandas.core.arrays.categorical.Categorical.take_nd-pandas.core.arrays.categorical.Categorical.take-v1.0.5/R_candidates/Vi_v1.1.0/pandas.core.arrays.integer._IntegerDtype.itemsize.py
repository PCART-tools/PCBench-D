    @cache_readonly
    def itemsize(self) -> int:
        """ Return the number of bytes in this dtype """
        return self.numpy_dtype.itemsize
