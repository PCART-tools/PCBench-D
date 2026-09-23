    @doc_wraps(np.random.RandomState.negative_binomial)
    def negative_binomial(self, n, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.negative_binomial, n, p,
                          size=size, chunks=chunks)
