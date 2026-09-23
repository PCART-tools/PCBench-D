    def to_frame(self, index=True):
        """
        Create a DataFrame with the columns the levels of the MultiIndex

        .. versionadded:: 0.20.0

        Parameters
        ----------
        index : boolean, default True
            return this MultiIndex as the index

        Returns
        -------
        DataFrame
        """

        from pandas import DataFrame
        result = DataFrame({(name or level):
                            self._get_level_values(level)
                            for name, level in
                            zip(self.names, range(len(self.levels)))},
                           copy=False)
        if index:
            result.index = self
        return result
