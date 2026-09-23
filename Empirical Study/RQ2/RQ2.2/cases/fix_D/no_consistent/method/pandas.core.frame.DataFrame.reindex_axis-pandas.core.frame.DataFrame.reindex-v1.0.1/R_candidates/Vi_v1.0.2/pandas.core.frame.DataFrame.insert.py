    def insert(self, loc, column, value, allow_duplicates=False) -> None:
        """
        Insert column into DataFrame at specified location.

        Raises a ValueError if `column` is already contained in the DataFrame,
        unless `allow_duplicates` is set to True.

        Parameters
        ----------
        loc : int
            Insertion index. Must verify 0 <= loc <= len(columns).
        column : str, number, or hashable object
            Label of the inserted column.
        value : int, Series, or array-like
        allow_duplicates : bool, optional
        """
        self._ensure_valid_index(value)
        value = self._sanitize_column(column, value, broadcast=False)
        self._data.insert(loc, column, value, allow_duplicates=allow_duplicates)
