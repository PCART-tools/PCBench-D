    def shift(self, periods, fill_value=None):
        """
        Shift Categorical by desired number of periods.

        Parameters
        ----------
        periods : int
            Number of periods to move, can be positive or negative
        fill_value : object, optional
            The scalar value to use for newly introduced missing values.

            .. versionadded:: 0.24.0

        Returns
        -------
        shifted : Categorical
        """
        # since categoricals always have ndim == 1, an axis parameter
        # doesn't make any sense here.
        codes = self.codes
        if codes.ndim > 1:
            raise NotImplementedError("Categorical with ndim > 1.")
        if np.prod(codes.shape) and (periods != 0):
            codes = np.roll(codes, ensure_platform_int(periods), axis=0)
            if isna(fill_value):
                fill_value = -1
            elif fill_value in self.categories:
                fill_value = self.categories.get_loc(fill_value)
            else:
                raise ValueError("'fill_value={}' is not present "
                                 "in this Categorical's "
                                 "categories".format(fill_value))
            if periods > 0:
                codes[:periods] = fill_value
            else:
                codes[periods:] = fill_value

        return self.from_codes(codes, dtype=self.dtype)
