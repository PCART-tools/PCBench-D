    @doc_wraps(np.random.RandomState.triangular)
    def triangular(self, left, mode, right, size=None, chunks=None):
        return self._wrap(np.random.RandomState.triangular, left, mode, right,
                          size=size, chunks=chunks)
