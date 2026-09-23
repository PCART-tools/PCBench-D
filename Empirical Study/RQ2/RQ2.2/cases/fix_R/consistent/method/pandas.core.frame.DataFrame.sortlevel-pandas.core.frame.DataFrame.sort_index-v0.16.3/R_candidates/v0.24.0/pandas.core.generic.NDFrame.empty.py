    @property
    def empty(self):
        """
        Indicator whether DataFrame is empty.

        True if DataFrame is entirely empty (no items), meaning any of the
        axes are of length 0.

        Returns
        -------
        bool
            If DataFrame is empty, return True, if not return False.

        See Also
        --------
        pandas.Series.dropna
        pandas.DataFrame.dropna

        Notes
        -----
        If DataFrame contains only NaNs, it is still not considered empty. See
        the example below.

        Examples
        --------
        An example of an actual empty DataFrame. Notice the index is empty:

        >>> df_empty = pd.DataFrame({'A' : []})
        >>> df_empty
        Empty DataFrame
        Columns: [A]
        Index: []
        >>> df_empty.empty
        True

        If we only have NaNs in our DataFrame, it is not considered empty! We
        will need to drop the NaNs to make the DataFrame empty:

        >>> df = pd.DataFrame({'A' : [np.nan]})
        >>> df
            A
        0 NaN
        >>> df.empty
        False
        >>> df.dropna().empty
        True
        """
        return any(len(self._get_axis(a)) == 0 for a in self._AXIS_ORDERS)
