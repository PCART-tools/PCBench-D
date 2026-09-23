    def shift(self, periods):
        """
        Shift Categorical by desired number of periods.

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative

        Returns
        -------
        shifted : Categorical
        """
        # since categoricals always have ndim == 1, an axis parameter
        # doesnt make any sense here.
        codes = self.codes
        if codes.ndim > 1:
            raise NotImplementedError("Categorical with ndim > 1.")
        if np.prod(codes.shape) and (periods != 0):
            codes = np.roll(codes, _ensure_platform_int(periods), axis=0)
            if periods > 0:
                codes[:periods] = -1
            else:
                codes[periods:] = -1

        return self.from_codes(codes, categories=self.categories,
                               ordered=self.ordered)
