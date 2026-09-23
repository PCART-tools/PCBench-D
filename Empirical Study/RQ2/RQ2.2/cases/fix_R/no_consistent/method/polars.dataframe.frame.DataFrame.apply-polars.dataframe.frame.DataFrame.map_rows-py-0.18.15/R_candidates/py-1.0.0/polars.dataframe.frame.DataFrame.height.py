    @property
    def height(self) -> int:
        """
        Get the number of rows.

        Returns
        -------
        int

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3, 4, 5]})
        >>> df.height
        5
        """
        return self._df.height()
