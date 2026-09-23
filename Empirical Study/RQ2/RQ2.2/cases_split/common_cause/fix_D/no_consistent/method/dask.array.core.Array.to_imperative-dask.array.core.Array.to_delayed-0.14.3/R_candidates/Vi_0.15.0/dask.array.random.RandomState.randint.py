    @doc_wraps(np.random.RandomState.randint)
    def randint(self, low, high=None, size=None, chunks=None):
        return self._wrap(np.random.RandomState.randint, low, high,
                          size=size, chunks=chunks)
