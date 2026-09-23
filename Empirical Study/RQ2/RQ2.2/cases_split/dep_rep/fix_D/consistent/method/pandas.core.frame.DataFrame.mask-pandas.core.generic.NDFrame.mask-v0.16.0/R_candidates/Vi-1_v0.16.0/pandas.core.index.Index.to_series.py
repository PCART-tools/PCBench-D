    def to_series(self, **kwargs):
        """
        Create a Series with both index and values equal to the index keys
        useful with map for returning an indexer based on an index

        Returns
        -------
        Series : dtype will be based on the type of the Index values.
        """

        from pandas import Series
        return Series(self._to_embed(), index=self, name=self.name)
