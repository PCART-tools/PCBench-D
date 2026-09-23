    @doc_wraps(np.random.RandomState.power)
    def power(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.power, a,
                          size=size, chunks=chunks)
