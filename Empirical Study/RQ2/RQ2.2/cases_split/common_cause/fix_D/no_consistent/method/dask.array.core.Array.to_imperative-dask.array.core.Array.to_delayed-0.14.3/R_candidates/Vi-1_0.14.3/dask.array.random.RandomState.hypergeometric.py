    @doc_wraps(np.random.RandomState.hypergeometric)
    def hypergeometric(self, ngood, nbad, nsample, size=None, chunks=None):
        return self._wrap(np.random.RandomState.hypergeometric,
                          ngood, nbad, nsample,
                          size=size, chunks=chunks)
