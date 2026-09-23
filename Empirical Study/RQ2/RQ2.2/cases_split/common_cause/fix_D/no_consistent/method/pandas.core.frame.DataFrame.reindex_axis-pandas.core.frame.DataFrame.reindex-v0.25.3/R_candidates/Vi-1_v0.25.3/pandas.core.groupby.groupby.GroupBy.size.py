    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def size(self):
        """
        Compute group sizes.

        Returns
        -------
        Series
            Number of rows in each group.
        """
        result = self.grouper.size()

        if isinstance(self.obj, Series):
            result.name = getattr(self.obj, "name", None)
        return result
