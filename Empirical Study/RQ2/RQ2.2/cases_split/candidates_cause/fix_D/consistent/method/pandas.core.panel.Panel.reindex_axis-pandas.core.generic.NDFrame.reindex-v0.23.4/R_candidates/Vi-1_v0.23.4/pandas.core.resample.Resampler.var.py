    def var(self, ddof=1, *args, **kwargs):
        """
        Compute variance of groups, excluding missing values

        Parameters
        ----------
        ddof : integer, default 1
        degrees of freedom
        """
        nv.validate_resampler_func('var', args, kwargs)
        return self._downsample('var', ddof=ddof)
