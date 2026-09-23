    @doc_wraps(np.random.RandomState.multinomial)
    def multinomial(self, n, pvals, size=None, chunks=None):
        return self._wrap(np.random.RandomState.multinomial, n, pvals,
                          size=size, chunks=chunks,
                          extra_chunks=((len(pvals),),))
