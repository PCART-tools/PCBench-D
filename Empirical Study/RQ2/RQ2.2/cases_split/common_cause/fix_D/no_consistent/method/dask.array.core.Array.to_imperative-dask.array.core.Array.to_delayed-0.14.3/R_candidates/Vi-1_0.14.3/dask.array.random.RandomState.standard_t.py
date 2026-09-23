    @doc_wraps(np.random.RandomState.standard_t)
    def standard_t(self, df, size=None, chunks=None):
        return self._wrap(np.random.RandomState.standard_t, df,
                          size=size, chunks=chunks)
