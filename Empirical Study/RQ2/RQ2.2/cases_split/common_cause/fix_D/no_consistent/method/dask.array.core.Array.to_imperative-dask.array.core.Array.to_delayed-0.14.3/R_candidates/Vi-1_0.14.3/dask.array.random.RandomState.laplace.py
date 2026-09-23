    @doc_wraps(np.random.RandomState.laplace)
    def laplace(self, loc=0.0, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.laplace, loc, scale,
                          size=size, chunks=chunks)
