    @doc_wraps(np.random.RandomState.wald)
    def wald(self, mean, scale, size=None, chunks=None):
        return self._wrap(np.random.RandomState.wald, mean, scale,
                          size=size, chunks=chunks)
