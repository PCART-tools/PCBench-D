    @doc_wraps(np.random.RandomState.exponential)
    def exponential(self, scale=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.exponential, scale,
                          size=size, chunks=chunks)
