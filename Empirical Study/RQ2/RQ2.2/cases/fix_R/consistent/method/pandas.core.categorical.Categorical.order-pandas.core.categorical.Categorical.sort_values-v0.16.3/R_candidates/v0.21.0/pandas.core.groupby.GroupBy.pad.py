    @Substitution(name='groupby')
    @Appender(_doc_template)
    def pad(self, limit=None):
        """
        Forward fill the values

        Parameters
        ----------
        limit : integer, optional
            limit of how many values to fill

        See Also
        --------
        Series.fillna
        DataFrame.fillna
        """
        return self.apply(lambda x: x.ffill(limit=limit))
