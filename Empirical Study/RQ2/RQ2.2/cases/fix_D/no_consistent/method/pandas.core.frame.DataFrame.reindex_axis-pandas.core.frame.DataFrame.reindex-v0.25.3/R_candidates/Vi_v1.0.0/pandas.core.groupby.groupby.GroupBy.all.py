    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def all(self, skipna: bool = True):
        """
        Return True if all values in the group are truthful, else False.

        Parameters
        ----------
        skipna : bool, default True
            Flag to ignore nan values during truth testing.

        Returns
        -------
        bool
        """
        return self._bool_agg("all", skipna)
