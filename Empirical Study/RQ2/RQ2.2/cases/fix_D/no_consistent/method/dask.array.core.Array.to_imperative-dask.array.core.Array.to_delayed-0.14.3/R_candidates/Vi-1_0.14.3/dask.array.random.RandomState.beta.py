    @doc_wraps(np.random.RandomState.beta)
    def beta(self, a, b, size=None, chunks=None):
        return self._wrap(np.random.RandomState.beta, a, b,
                          size=size, chunks=chunks)
