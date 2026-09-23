    @doc_wraps(np.random.RandomState.vonmises)
    def vonmises(self, mu, kappa, size=None, chunks=None):
        return self._wrap(np.random.RandomState.vonmises, mu, kappa,
                          size=size, chunks=chunks)
