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

        fill_value = self._validate_fill_value(fill_value)

        codes = shift(codes, periods, axis=0, fill_value=fill_value)

        return self._constructor(codes, dtype=self.dtype, fastpath=True)
