    def to_series(self, keep_tz=False):
        """
        Create a Series with both index and values equal to the index keys
        useful with map for returning an indexer based on an index

        Parameters
        ----------
        keep_tz : optional, defaults False.
                  applies only to a DatetimeIndex

        Returns
        -------
        Series : dtype will be based on the type of the Index values.
        """

        import pandas as pd
        values = self._to_embed(keep_tz)
        return pd.Series(values, index=self, name=self.name)
