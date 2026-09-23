    @doc_wraps(np.random.RandomState.poisson)
    def poisson(self, lam=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.poisson, lam,
                          size=size, chunks=chunks)
