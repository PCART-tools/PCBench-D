    @doc_wraps(np.random.RandomState.random_integers)
    def random_integers(self, low, high=None, size=None, chunks=None):
        return self._wrap(np.random.RandomState.random_integers, low, high,
                          size=size, chunks=chunks)
