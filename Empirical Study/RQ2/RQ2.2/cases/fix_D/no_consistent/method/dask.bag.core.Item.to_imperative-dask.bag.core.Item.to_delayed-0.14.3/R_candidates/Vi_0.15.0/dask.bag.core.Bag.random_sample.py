    def random_sample(self, prob, random_state=None):
        """ Return elements from bag with probability of ``prob``.

        Parameters
        ----------
        prob : float
            A float between 0 and 1, representing the probability that each
            element will be returned.
        random_state : int or random.Random, optional
            If an integer, will be used to seed a new ``random.Random`` object.
            If provided, results in deterministic sampling.

        Examples
        --------
        >>> import dask.bag as db
        >>> b = db.from_sequence(range(5))
        >>> list(b.random_sample(0.5, 42))
        [1, 4]
        >>> list(b.random_sample(0.5, 42))
        [1, 4]
        """
        if not 0 <= prob <= 1:
            raise ValueError('prob must be a number in the interval [0, 1]')
        if not isinstance(random_state, Random):
            random_state = Random(random_state)

        name = 'random-sample-%s' % tokenize(self, prob, random_state.getstate())
        state_data = random_state_data_python(self.npartitions, random_state)
        dsk = {(name, i): (reify, (random_sample, (self.name, i), state, prob))
               for i, state in zip(range(self.npartitions), state_data)}
        return type(self)(merge(self.dask, dsk), name, self.npartitions)
