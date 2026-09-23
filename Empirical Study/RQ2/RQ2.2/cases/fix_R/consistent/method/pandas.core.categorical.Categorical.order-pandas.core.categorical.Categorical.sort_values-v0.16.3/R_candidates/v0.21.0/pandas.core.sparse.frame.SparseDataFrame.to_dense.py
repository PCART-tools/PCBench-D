    def to_dense(self):
        """
        Convert to dense DataFrame

        Returns
        -------
        df : DataFrame
        """
        data = dict((k, v.to_dense()) for k, v in compat.iteritems(self))
        return DataFrame(data, index=self.index, columns=self.columns)
