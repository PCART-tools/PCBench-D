    def lower_bound(self) -> Self:
        """
        Return the lower bound of this Series' dtype as a unit Series.

        See Also
        --------
        upper_bound : return the upper bound of the given Series' dtype.

        Examples
        --------
        >>> s = pl.Series("s", [-1, 0, 1], dtype=pl.Int32)
        >>> s.lower_bound()
        shape: (1,)
        Series: 's' [i32]
        [
            -2147483648
        ]

        >>> s = pl.Series("s", [1.0, 2.5, 3.0], dtype=pl.Float32)
        >>> s.lower_bound()
        shape: (1,)
        Series: 's' [f32]
        [
            -inf
        ]

        """
