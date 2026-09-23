    @cache_readonly
    def is_unique(self):
        """
        Return True if the IntervalIndex contains unique elements, else False
        """
        return self._multiindex.is_unique
