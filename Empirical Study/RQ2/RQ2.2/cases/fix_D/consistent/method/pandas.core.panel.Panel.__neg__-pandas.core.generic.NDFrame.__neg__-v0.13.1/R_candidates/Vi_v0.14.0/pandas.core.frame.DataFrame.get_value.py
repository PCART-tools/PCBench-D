    def get_value(self, index, col, takeable=False):
        """
        Quickly retrieve single value at passed column and index

        Parameters
        ----------
        index : row label
        col : column label
        takeable : interpret the index/col as indexers, default False

        Returns
        -------
        value : scalar value
        """

        if takeable is True:
            series = self._iget_item_cache(col)
            return series.values[index]

        series = self._get_item_cache(col)
        engine = self.index._engine
        return engine.get_value(series.values, index)
