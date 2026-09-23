    def set_params(self, **kwargs):
        """Set parameters within this locator."""
        if 'nbins' in kwargs:
            self._nbins = kwargs['nbins']
            if self._nbins != 'auto':
                self._nbins = int(self._nbins)
        if 'trim' in kwargs:
            warnings.warn(
                "The 'trim' keyword has no effect since version 2.0.",
                mplDeprecation)
        if 'symmetric' in kwargs:
            self._symmetric = kwargs['symmetric']
        if 'prune' in kwargs:
            prune = kwargs['prune']
            if prune is not None and prune not in ['upper', 'lower', 'both']:
                raise ValueError(
                    "prune must be 'upper', 'lower', 'both', or None")
            self._prune = prune
        if 'min_n_ticks' in kwargs:
            self._min_n_ticks = max(1, kwargs['min_n_ticks'])
        if 'steps' in kwargs:
            steps = kwargs['steps']
            if steps is None:
                self._steps = np.array([1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10])
            else:
                self._steps = self._validate_steps(steps)
            self._extended_steps = self._staircase(self._steps)
        if 'integer' in kwargs:
            self._integer = kwargs['integer']
