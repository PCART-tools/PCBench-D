    @doc_wraps(np.random.RandomState.weibull)
    def weibull(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.weibull, a,
                          size=size, chunks=chunks)
