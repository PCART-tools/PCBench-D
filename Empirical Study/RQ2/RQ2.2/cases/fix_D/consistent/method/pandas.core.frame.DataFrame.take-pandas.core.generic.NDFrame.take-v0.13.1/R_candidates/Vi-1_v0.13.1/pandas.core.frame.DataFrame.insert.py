    def insert(self, loc, column, value, allow_duplicates=False):
        """
        Insert column into DataFrame at specified location.

        If `allow_duplicates` is False, raises Exception if column
        is already contained in the DataFrame.

        Parameters
        ----------
        loc : int
            Must have 0 <= loc <= len(columns)
        column : object
        value : int, Series, or array-like
        """
        self._ensure_valid_index(value)
        value = self._sanitize_column(column, value)
        self._data.insert(
            loc, column, value, allow_duplicates=allow_duplicates)
