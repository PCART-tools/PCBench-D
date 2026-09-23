    @doc_wraps(np.random.RandomState.standard_cauchy)
    def standard_cauchy(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_cauchy,
                          size=size, chunks=chunks)
