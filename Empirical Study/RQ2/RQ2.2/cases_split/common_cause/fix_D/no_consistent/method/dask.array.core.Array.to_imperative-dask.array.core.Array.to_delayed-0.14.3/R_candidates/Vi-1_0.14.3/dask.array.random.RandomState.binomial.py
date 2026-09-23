    @doc_wraps(np.random.RandomState.binomial)
    def binomial(self, n, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.binomial, n, p,
                          size=size, chunks=chunks)
