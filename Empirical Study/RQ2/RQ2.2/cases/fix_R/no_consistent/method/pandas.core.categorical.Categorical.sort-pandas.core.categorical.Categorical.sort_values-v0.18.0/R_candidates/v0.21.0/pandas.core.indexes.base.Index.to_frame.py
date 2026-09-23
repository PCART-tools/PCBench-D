    def to_frame(self, index=True):
        """
        Create a DataFrame with a column containing the Index.

        .. versionadded:: 0.21.0

        Parameters
        ----------
        index : boolean, default True
            Set the index of the returned DataFrame as the original Index.

        Returns
        -------
        DataFrame : a DataFrame containing the original Index data.
        """

        from pandas import DataFrame
        result = DataFrame(self._shallow_copy(), columns=[self.name or 0])

        if index:
            result.index = self
        return result
