        @doc_wraps(np.random.RandomState.choice)
        def choice(self, a, size=None, replace=True, p=None, chunks=None):
            return self._wrap(np.random.RandomState.choice, a,
                              size=size, replace=True, p=None, chunks=chunks)
