    @cache_readonly
    def _tuple_index(self):
        """
        Convert MultiIndex to an Index of tuples

        Returns
        -------
        index : Index
        """
        return Index(self.values)
