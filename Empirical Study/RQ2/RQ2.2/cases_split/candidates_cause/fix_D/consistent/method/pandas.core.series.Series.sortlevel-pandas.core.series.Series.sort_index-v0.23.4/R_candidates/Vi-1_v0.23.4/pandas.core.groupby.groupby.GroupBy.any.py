    @Substitution(name='groupby')
    @Appender(_doc_template)
    def any(self, skipna=True):
        """
        Returns True if any value in the group is truthful, else False

        Parameters
        ----------
        skipna : bool, default True
            Flag to ignore nan values during truth testing
        """
        return self._bool_agg('any', skipna)
