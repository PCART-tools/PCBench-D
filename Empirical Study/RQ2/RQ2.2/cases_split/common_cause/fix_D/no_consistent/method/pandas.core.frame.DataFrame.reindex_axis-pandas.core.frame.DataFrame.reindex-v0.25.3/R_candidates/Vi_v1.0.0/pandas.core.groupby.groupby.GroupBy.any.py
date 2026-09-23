    @Substitution(name="groupby")
    @Appender(_common_see_also)
    def any(self, skipna: bool = True):
        """
        Return True if any value in the group is truthful, else False.

        Parameters
        ----------
        skipna : bool, default True
            Flag to ignore nan values during truth testing.

        Returns
        -------
        bool
        """
        return self._bool_agg("any", skipna)
