    @Substitution(name='groupby')
    @Appender(_common_see_also)
    def sem(self, ddof=1):
        """
        Compute standard error of the mean of groups, excluding missing values.

        For multiple groupings, the result index will be a MultiIndex.

        Parameters
        ----------
        ddof : integer, default 1
            degrees of freedom
        """

        return self.std(ddof=ddof) / np.sqrt(self.count())
