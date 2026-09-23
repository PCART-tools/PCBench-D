    @cache_readonly
    def numpy_dtype(self) -> np.dtype:
        """ Return an instance of our numpy dtype """
        return np.dtype(self.type)
