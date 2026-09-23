    @doc_wraps(np.random.RandomState.chisquare)
    def chisquare(self, df, size=None, chunks=None):
        return self._wrap(np.random.RandomState.chisquare, df,
                          size=size, chunks=chunks)
