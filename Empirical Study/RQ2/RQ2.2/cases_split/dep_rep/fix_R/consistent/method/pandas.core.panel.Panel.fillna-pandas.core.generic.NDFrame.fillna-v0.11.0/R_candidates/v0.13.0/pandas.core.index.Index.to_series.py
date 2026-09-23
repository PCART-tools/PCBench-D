    def to_series(self):
        """
        return a series with both index and values equal to the index keys
        useful with map for returning an indexer based on an index
        """
        import pandas as pd
        return pd.Series(self.values, index=self, name=self.name)
