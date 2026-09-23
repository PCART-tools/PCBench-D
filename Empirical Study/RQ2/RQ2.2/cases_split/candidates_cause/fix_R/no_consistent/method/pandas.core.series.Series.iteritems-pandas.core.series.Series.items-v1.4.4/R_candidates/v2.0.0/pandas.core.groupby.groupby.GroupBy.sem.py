    @final
    def sem(self, ddof: int = 1, numeric_only: bool = False):
        """
        Compute standard error of the mean of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

        numeric_only : bool, default False
            Include only `float`, `int` or `boolean` data.

            .. versionadded:: 1.5.0

            .. versionchanged:: 2.0.0

                numeric_only now defaults to ``False``.

        Returns
        -------
        Series or DataFrame
            Standard error of the mean of values within each group.
        """
        if numeric_only and self.obj.ndim == 1 and not is_numeric_dtype(self.obj.dtype):
            raise TypeError(
                f"{type(self).__name__}.sem called with "
                f"numeric_only={numeric_only} and dtype {self.obj.dtype}"
            )
        result = self.std(ddof=ddof, numeric_only=numeric_only)

        if result.ndim == 1:
            result /= np.sqrt(self.count())
        else:
            cols = result.columns.difference(self.exclusions).unique()
            counts = self.count()
            result_ilocs = result.columns.get_indexer_for(cols)
            count_ilocs = counts.columns.get_indexer_for(cols)

            result.iloc[:, result_ilocs] /= np.sqrt(counts.iloc[:, count_ilocs])
        return result
