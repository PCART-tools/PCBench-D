    @doc_wraps(np.random.RandomState.gamma)
    def gamma(self, shape, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.gamma, shape, scale,
                          size=size, chunks=chunks)
