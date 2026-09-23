    @doc_wraps(np.random.RandomState.tomaxint)
    def tomaxint(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.tomaxint,
                          size=size, chunks=chunks)
