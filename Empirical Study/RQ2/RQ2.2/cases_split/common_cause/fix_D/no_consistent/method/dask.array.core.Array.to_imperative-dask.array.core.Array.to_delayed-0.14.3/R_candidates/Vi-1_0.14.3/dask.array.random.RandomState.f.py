    @doc_wraps(np.random.RandomState.f)
    def f(self, dfnum, dfden, size=None, chunks=None):
        return self._wrap(np.random.RandomState.f, dfnum, dfden,
                          size=size, chunks=chunks)
