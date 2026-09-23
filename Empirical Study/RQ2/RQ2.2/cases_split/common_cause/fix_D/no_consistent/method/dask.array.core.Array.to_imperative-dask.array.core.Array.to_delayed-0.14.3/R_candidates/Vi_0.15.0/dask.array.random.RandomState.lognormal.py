    @doc_wraps(np.random.RandomState.lognormal)
    def lognormal(self, mean=0.0, sigma=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.lognormal, mean, sigma,
                          size=size, chunks=chunks)
