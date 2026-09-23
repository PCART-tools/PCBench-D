    @property
    def is_unique(self) -> bool:
        """
        Return boolean if values in the object are unique.

        Returns
        -------
        bool

        Examples
        --------
        >>> s = pd.Series([1, 2, 3])
        >>> s.is_unique
        True

        >>> s = pd.Series([1, 2, 3, 1])
        >>> s.is_unique
        False
        """
        return self.nunique(dropna=False) == len(self)
