    @doc_wraps(np.random.RandomState.rayleigh)
    def rayleigh(self, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.rayleigh, scale,
                          size=size, chunks=chunks)
