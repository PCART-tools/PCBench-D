    def upper_bound(self) -> Self:
        """
        Return the upper bound of this Series' dtype as a unit Series.

        See Also
        --------
        lower_bound : return the lower bound of the given Series' dtype.

        Examples
        --------
        >>> s = pl.Series("s", [-1, 0, 1], dtype=pl.Int8)
        >>> s.upper_bound()
        shape: (1,)
        Series: 's' [i8]
        [
            127
        ]

        >>> s = pl.Series("s", [1.0, 2.5, 3.0], dtype=pl.Float64)
        >>> s.upper_bound()
        shape: (1,)
        Series: 's' [f64]
        [
            inf
        ]

        """
