    def var(self, ddof=1, *args, **kwargs):
        """
        Compute variance of groups, excluding missing values.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

        Returns
        -------
        DataFrame or Series
            Variance of values within each group.
        """
        nv.validate_resampler_func("var", args, kwargs)
        return self._downsample("var", ddof=ddof)
