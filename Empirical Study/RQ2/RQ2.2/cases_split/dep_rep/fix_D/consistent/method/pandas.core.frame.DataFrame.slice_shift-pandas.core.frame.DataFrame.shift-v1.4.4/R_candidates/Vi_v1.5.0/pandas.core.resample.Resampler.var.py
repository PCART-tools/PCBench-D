    def var(
        self,
        ddof=1,
        numeric_only: bool | lib.NoDefault = lib.no_default,
        *args,
        **kwargs,
    ):
        """
        Compute variance of groups, excluding missing values.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

        numeric_only : bool, default False
            Include only `float`, `int` or `boolean` data.

            .. versionadded:: 1.5.0

        Returns
        -------
        DataFrame or Series
            Variance of values within each group.
        """
        nv.validate_resampler_func("var", args, kwargs)
        return self._downsample("var", ddof=ddof, numeric_only=numeric_only)
