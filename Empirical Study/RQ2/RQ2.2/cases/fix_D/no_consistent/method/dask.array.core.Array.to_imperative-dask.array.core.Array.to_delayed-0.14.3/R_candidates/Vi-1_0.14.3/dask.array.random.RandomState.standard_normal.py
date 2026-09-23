    @doc_wraps(np.random.RandomState.standard_normal)
    def standard_normal(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_normal,
                          size=size, chunks=chunks)
