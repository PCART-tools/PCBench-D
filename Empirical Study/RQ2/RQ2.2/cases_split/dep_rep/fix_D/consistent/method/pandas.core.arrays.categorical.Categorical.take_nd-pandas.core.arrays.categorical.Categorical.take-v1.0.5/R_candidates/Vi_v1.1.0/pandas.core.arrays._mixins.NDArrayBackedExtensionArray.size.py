    @cache_readonly
    def size(self) -> int:
        return np.prod(self.shape)
