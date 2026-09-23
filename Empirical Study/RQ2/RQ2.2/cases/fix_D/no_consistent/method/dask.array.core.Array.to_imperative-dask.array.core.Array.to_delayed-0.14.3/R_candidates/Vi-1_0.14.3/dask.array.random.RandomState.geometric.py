    @doc_wraps(np.random.RandomState.geometric)
    def geometric(self, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.geometric, p,
                          size=size, chunks=chunks)
