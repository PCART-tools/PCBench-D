    @doc_wraps(np.random.RandomState.noncentral_f)
    def noncentral_f(self, dfnum, dfden, nonc,  size=None, chunks=None):
        return self._wrap(np.random.RandomState.noncentral_f,
                          dfnum, dfden, nonc,
                          size=size, chunks=chunks)
