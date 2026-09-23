    def limit(self, n: int = 10) -> Series:
        """
        Get the first `n` elements.

        Alias for :func:`Series.head`.

        Parameters
        ----------
        n
            Number of elements to return. If a negative value is passed, return all
            elements except the last `abs(n)`.

        See Also
        --------
        head

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3, 4, 5])
        >>> s.limit(3)
        shape: (3,)
        Series: 'a' [i64]
        [
            1
            2
            3
        ]

        Pass a negative value to get all rows `except` the last `abs(n)`.

        >>> s.limit(-3)
        shape: (2,)
        Series: 'a' [i64]
        [
                1
                2
        ]
        """
        return self.head(n)
