    @cache_readonly
    def ndim(self):
        """Number of dimensions of the Categorical """
        return self._codes.ndim
