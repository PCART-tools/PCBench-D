    def to_dense(self):
        """
        Convert SparseSeries to a Series.

        Returns
        -------
        s : Series
        """
        return Series(self.values.to_dense(), index=self.index, name=self.name)
