    @doc_wraps(np.random.RandomState.zipf)
    def zipf(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.zipf, a,
                          size=size, chunks=chunks)
