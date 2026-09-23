    @cache_readonly
    def numpy_dtype(self):
        """ Return an instance of our numpy dtype """
        return np.dtype(self.type)
