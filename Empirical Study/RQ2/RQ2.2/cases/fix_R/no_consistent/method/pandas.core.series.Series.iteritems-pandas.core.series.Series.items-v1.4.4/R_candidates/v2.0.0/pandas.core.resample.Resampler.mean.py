    def mean(
        self,
        numeric_only: bool = False,
        *args,
        **kwargs,
    ):
        """
        Compute mean of groups, excluding missing values.

        Parameters
        ----------
        numeric_only : bool, default False
            Include only `float`, `int` or `boolean` data.

            .. versionchanged:: 2.0.0

                numeric_only now defaults to ``False``.

        Returns
        -------
        DataFrame or Series
            Mean of values within each group.
        """
        maybe_warn_args_and_kwargs(type(self), "mean", args, kwargs)
        nv.validate_resampler_func("mean", args, kwargs)
        return self._downsample("mean", numeric_only=numeric_only)
