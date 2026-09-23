    def std(self, ddof=1, *args, **kwargs):
        """
        Compute standard deviation of groups, excluding missing values.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

        Returns
        -------
        DataFrame or Series
            Standard deviation of values within each group.
        """
        nv.validate_resampler_func("std", args, kwargs)
        # error: Unexpected keyword argument "ddof" for "_downsample"
        return self._downsample("std", ddof=ddof)  # type: ignore[call-arg]
