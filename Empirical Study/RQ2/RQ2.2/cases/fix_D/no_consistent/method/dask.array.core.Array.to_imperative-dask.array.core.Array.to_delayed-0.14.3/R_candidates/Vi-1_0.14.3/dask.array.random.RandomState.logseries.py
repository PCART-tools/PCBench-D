    @doc_wraps(np.random.RandomState.logseries)
    def logseries(self, p, size=None, chunks=None):
        return self._wrap(np.random.RandomState.logseries, p,
                          size=size, chunks=chunks)
