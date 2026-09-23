    @doc_wraps(np.random.RandomState.pareto)
    def pareto(self, a, size=None, chunks=None):
        return self._wrap(np.random.RandomState.pareto, a,
                          size=size, chunks=chunks)
