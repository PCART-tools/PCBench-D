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
        DataFrame
            DataFrame containing the original Index data.

        See Also
        --------
        Index.to_series : Convert an Index to a Series.
        Series.to_frame : Convert Series to DataFrame.

        Examples
        --------
        >>> idx = pd.Index(['Ant', 'Bear', 'Cow'], name='animal')
        >>> idx.to_frame()
               animal
        animal
        Ant       Ant
        Bear     Bear
        Cow       Cow

        By default, the original Index is reused. To enforce a new Index:

        >>> idx.to_frame(index=False)
            animal
        0   Ant
        1  Bear
        2   Cow
        """

        from pandas import DataFrame
        result = DataFrame(self._shallow_copy(), columns=[self.name or 0])

        if index:
            result.index = self
        return result
