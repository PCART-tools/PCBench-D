    def to_frame(self, index=True):
        """
        Create a DataFrame with the levels of the MultiIndex as columns.

        .. versionadded:: 0.20.0

        Parameters
        ----------
        index : boolean, default True
            Set the index of the returned DataFrame as the original MultiIndex.

        Returns
        -------
        DataFrame : a DataFrame containing the original MultiIndex data.
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
