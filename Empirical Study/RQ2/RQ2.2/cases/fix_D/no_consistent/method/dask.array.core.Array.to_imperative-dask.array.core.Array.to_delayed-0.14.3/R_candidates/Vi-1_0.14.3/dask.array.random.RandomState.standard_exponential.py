    @doc_wraps(np.random.RandomState.standard_exponential)
    def standard_exponential(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_exponential,
                          size=size, chunks=chunks)
