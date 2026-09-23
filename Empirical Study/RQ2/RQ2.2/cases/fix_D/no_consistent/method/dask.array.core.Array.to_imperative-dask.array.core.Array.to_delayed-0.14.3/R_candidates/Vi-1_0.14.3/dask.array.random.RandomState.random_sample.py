    @doc_wraps(np.random.RandomState.random_sample)
    def random_sample(self, size=None, chunks=None):
        return self._wrap(np.random.RandomState.random_sample,
                          size=size, chunks=chunks)
