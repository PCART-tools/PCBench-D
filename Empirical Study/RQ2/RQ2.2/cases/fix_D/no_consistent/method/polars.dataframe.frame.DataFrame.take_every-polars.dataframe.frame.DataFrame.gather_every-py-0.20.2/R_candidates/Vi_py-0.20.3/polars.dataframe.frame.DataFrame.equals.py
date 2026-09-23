    def equals(self, other: DataFrame, *, null_equal: bool = True) -> bool:
        """
        Check whether the DataFrame is equal to another DataFrame.

        Parameters
        ----------
        other
            DataFrame to compare with.
        null_equal
            Consider null values as equal.

        See Also
        --------
        assert_frame_equal

        Examples
        --------
        >>> df1 = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )
        >>> df2 = pl.DataFrame(
        ...     {
        ...         "foo": [3, 2, 1],
        ...         "bar": [8.0, 7.0, 6.0],
        ...         "ham": ["c", "b", "a"],
        ...     }
        ... )
        >>> df1.equals(df1)
        True
        >>> df1.equals(df2)
        False

        """
        return self._df.equals(other._df, null_equal)
