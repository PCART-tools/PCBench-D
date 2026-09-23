    def get_value(self, series, key):
        """
        Fast lookup of value from 1-dimensional ndarray. Only use this if you
        know what you're doing
        """
        try:
            k = com._values_from_object(key)
            k = self._convert_scalar_indexer(k, kind='getitem')
            indexer = self.get_loc(k)
            return series.iloc[indexer]
        except (KeyError, TypeError):
            pass

        # we might be a positional inexer
        return super(CategoricalIndex, self).get_value(series, key)
