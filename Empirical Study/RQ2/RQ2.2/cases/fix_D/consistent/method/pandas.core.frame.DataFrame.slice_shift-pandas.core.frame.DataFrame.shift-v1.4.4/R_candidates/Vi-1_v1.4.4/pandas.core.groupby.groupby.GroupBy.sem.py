    @final
    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def sem(self, ddof: int = 1):
        """
        Compute standard error of the mean of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : int, default 1
            Degrees of freedom.

        Returns
        -------
        Series or DataFrame
            Standard error of the mean of values within each group.
        """
        result = self.std(ddof=ddof)
        if result.ndim == 1:
            result /= np.sqrt(self.count())
        else:
            cols = result.columns.difference(self.exclusions).unique()
            counts = self.count()
            result_ilocs = result.columns.get_indexer_for(cols)
            count_ilocs = counts.columns.get_indexer_for(cols)
            result.iloc[:, result_ilocs] /= np.sqrt(counts.iloc[:, count_ilocs])
        return result
