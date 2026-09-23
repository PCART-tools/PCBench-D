    def top_k(self, k: int = 5) -> Series:
        r"""
        Return the `k` largest elements.

        Non-null elements are always preferred over null elements. The output is
        not guaranteed to be in any particular order, call :func:`sort` after
        this function if you wish the output to be sorted.

        This has time complexity:

        .. math:: O(n)

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
