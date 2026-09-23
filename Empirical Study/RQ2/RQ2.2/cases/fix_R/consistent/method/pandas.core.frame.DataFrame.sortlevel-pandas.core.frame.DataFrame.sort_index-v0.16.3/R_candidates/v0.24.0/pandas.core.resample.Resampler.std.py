    def std(self, ddof=1, *args, **kwargs):
        """
        Compute standard deviation of groups, excluding missing values.

        Parameters
        ----------
        ddof : integer, default 1
        degrees of freedom
        """
        nv.validate_resampler_func('std', args, kwargs)
        return self._downsample('std', ddof=ddof)
