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
        return self._downsample("std", ddof=ddof)
