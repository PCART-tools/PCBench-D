    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def count(self):
        """
        Compute count of group, excluding missing values.

        Returns
        -------
        Series or DataFrame
            Count of values within each group.
        """

        # defined here for API doc
        raise NotImplementedError
