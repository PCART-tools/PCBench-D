    def __getitem__(self, key):
        """
        Retrieve column or slice from DataFrame
        """
        if isinstance(key, slice):
            date_rng = self.index[key]
            return self.reindex(date_rng)
        elif isinstance(key, (np.ndarray, list, Series)):
            return self._getitem_array(key)
        else:
            return self._get_item_cache(key)
