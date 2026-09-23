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
        # error: Unexpected keyword argument "ddof" for "_downsample"
        return self._downsample("var", ddof=ddof)  # type: ignore[call-arg]
