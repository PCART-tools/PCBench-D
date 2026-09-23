    @doc_wraps(np.random.RandomState.uniform)
    def uniform(self, low=0.0, high=1.0, size=None, chunks=None):
        return self._wrap(np.random.RandomState.uniform, low, high,
                          size=size, chunks=chunks)
