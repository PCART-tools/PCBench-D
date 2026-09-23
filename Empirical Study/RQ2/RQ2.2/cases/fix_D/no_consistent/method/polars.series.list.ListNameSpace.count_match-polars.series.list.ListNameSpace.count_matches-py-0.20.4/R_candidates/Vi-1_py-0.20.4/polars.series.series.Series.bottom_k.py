    def bottom_k(self, k: int | IntoExprColumn = 5) -> Series:
        r"""
        Return the `k` smallest elements.

        This has time complexity:

        .. math:: O(n + k \\log{}n - \frac{k}{2})

        Parameters
        ----------
        k
            Number of elements to return.

        See Also
        --------
        top_k

        Examples
        --------
        >>> s = pl.Series("a", [2, 5, 1, 4, 3])
        >>> s.bottom_k(3)
        shape: (3,)
        Series: 'a' [i64]
        [
            1
            2
            3
        ]
        """
