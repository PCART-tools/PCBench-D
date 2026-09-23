    @doc_wraps(np.random.RandomState.noncentral_chisquare)
    def noncentral_chisquare(self, df, nonc, size=None, chunks=None):
        return self._wrap(np.random.RandomState.noncentral_chisquare, df, nonc,
                          size=size, chunks=chunks)
