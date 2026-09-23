    def top_k(self, k: int = 5) -> Series:
        r"""
        Return the `k` largest elements.

        This has time complexity:

        .. math:: O(n + k \log{n})

        Parameters
        ----------
        k
            Number of elements to return.

        See Also
        --------
        bottom_k

        Examples
        --------
        >>> s = pl.Series("a", [2, 5, 1, 4, 3])
        >>> s.top_k(3)
        shape: (3,)
        Series: 'a' [i64]
        [
            5
            4
            3
        ]
        """
