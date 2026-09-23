    def set_value(self, index, col, value):
        """
        Put single value at passed column and index

        Parameters
        ----------
        index : row label
        col : column label
        value : scalar value

        Returns
        -------
        frame : DataFrame
            If label pair is contained, will be reference to calling DataFrame,
            otherwise a new object
        """
        try:
            series = self._get_item_cache(col)
            engine = self.index._engine
            engine.set_value(series.values, index, value)
            return self
        except KeyError:

            # set using a non-recursive method & reset the cache
            self.loc[index, col] = value
            self._item_cache.pop(col, None)

            return self
