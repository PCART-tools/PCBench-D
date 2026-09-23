    @property
    def nlevels(self) -> int:
        """
        Integer number of levels in this MultiIndex.
        """
        return len(self._levels)
