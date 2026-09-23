    def droplevel(self, level, axis=0):
        """
        Return DataFrame with requested index / column level(s) removed.

        .. versionadded:: 0.24.0

        Parameters
        ----------
        level : int, str, or list-like
            If a string is given, must be the name of a level
            If list-like, elements must be names or positional indexes
            of levels.

        axis : {0 or 'index', 1 or 'columns'}, default 0

        Returns
        -------
        DataFrame.droplevel()

        Examples
        --------
        >>> df = pd.DataFrame([
        ...     [1, 2, 3, 4],
        ...     [5, 6, 7, 8],
        ...     [9, 10, 11, 12]
        ... ]).set_index([0, 1]).rename_axis(['a', 'b'])

        >>> df.columns = pd.MultiIndex.from_tuples([
        ...    ('c', 'e'), ('d', 'f')
        ... ], names=['level_1', 'level_2'])

        >>> df
        level_1   c   d
        level_2   e   f
        a b
        1 2      3   4
        5 6      7   8
        9 10    11  12

        >>> df.droplevel('a')
        level_1   c   d
        level_2   e   f
        b
        2        3   4
        6        7   8
        10      11  12

        >>> df.droplevel('level2', axis=1)
        level_1   c   d
        a b
        1 2      3   4
        5 6      7   8
        9 10    11  12
        """
        labels = self._get_axis(axis)
        new_labels = labels.droplevel(level)
        result = self.set_axis(new_labels, axis=axis, inplace=False)
        return result
