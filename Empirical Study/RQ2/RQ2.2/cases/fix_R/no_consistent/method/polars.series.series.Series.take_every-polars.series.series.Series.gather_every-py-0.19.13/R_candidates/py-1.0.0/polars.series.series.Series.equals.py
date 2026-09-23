    @deprecate_renamed_parameter("strict", "check_dtypes", version="0.20.31")
    def equals(
        self,
        other: Series,
        *,
        check_dtypes: bool = False,
        check_names: bool = False,
        null_equal: bool = True,
    ) -> bool:
        """
        Check whether the Series is equal to another Series.

        Parameters
        ----------
        other
            Series to compare with.
        check_dtypes
            Require data types to match.
        check_names
            Require names to match.
        null_equal
            Consider null values as equal.

        See Also
        --------
        assert_series_equal

        Examples
        --------
        >>> s1 = pl.Series("a", [1, 2, 3])
        >>> s2 = pl.Series("b", [4, 5, 6])
        >>> s1.equals(s1)
        True
        >>> s1.equals(s2)
        False
        """
        return self._s.equals(
            other._s,
            check_dtypes=check_dtypes,
            check_names=check_names,
            null_equal=null_equal,
        )
