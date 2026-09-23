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
            result.name = self.obj.name
        return self._reindex_output(result, fill_value=0)
