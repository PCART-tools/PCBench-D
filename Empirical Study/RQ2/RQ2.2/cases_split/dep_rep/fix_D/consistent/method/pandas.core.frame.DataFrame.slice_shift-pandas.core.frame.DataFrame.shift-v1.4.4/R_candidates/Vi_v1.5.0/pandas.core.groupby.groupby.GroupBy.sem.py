    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def sem(self, ddof: int = 1, numeric_only: bool | lib.NoDefault = lib.no_default):
        """
        Compute standard error of the mean of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

        numeric_only : bool, default True
            Include only `float`, `int` or `boolean` data.

            .. versionadded:: 1.5.0

        Returns
        -------
        Series or DataFrame
            Standard error of the mean of values within each group.
        """
        # Reolve numeric_only so that std doesn't warn
        numeric_only_bool = self._resolve_numeric_only("sem", numeric_only, axis=0)
        if (
            numeric_only_bool
            and self.obj.ndim == 1
            and not is_numeric_dtype(self.obj.dtype)
        ):
            raise TypeError(
                f"{type(self).__name__}.sem called with "
                f"numeric_only={numeric_only} and dtype {self.obj.dtype}"
            )
        result = self.std(ddof=ddof, numeric_only=numeric_only_bool)
        self._maybe_warn_numeric_only_depr("sem", result, numeric_only)

        if result.ndim == 1:
            result /= np.sqrt(self.count())
        else:
            cols = result.columns.difference(self.exclusions).unique()
            counts = self.count()
            result_ilocs = result.columns.get_indexer_for(cols)
            count_ilocs = counts.columns.get_indexer_for(cols)
            with warnings.catch_warnings():
                # TODO(2.0): once iloc[:, foo] = bar depecation is enforced,
                #  this catching will be unnecessary
                warnings.filterwarnings(
                    "ignore", ".*will attempt to set the values inplace.*"
                )
                result.iloc[:, result_ilocs] /= np.sqrt(counts.iloc[:, count_ilocs])
        return result
