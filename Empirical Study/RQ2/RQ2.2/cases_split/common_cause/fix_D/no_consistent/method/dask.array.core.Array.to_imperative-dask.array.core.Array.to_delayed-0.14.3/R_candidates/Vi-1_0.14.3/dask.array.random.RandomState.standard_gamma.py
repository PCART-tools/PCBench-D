    @doc_wraps(np.random.RandomState.standard_gamma)
    def standard_gamma(self, shape, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_gamma, shape,
                          size=size, chunks=chunks)
