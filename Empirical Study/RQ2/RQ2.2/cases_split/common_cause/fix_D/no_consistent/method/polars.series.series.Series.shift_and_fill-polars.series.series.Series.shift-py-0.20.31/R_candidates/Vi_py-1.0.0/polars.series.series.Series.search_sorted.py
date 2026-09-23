    def search_sorted(
        self,
        element: IntoExpr | np.ndarray[Any, Any] | None,
        side: SearchSortedSide = "any",
    ) -> int | Series:
        """
        Find indices where elements should be inserted to maintain order.

        .. math:: a[i-1] < v <= a[i]

        Parameters
        ----------
        element
            Expression or scalar value.
        side : {'any', 'left', 'right'}
            If 'any', the index of the first suitable location found is given.
            If 'left', the index of the leftmost suitable location found is given.
            If 'right', return the rightmost suitable location found is given.

        Examples
        --------
        >>> s = pl.Series("set", [1, 2, 3, 4, 4, 5, 6, 7])
        >>> s.search_sorted(4)
        3
        >>> s.search_sorted(4, "left")
        3
        >>> s.search_sorted(4, "right")
        5
        >>> s.search_sorted([1, 4, 5])
        shape: (3,)
        Series: 'set' [u32]
        [
                0
                3
                5
        ]
        >>> s.search_sorted([1, 4, 5], "left")
        shape: (3,)
        Series: 'set' [u32]
        [
                0
                3
                5
        ]
        >>> s.search_sorted([1, 4, 5], "right")
        shape: (3,)
        Series: 'set' [u32]
        [
                1
                5
                6
        ]
        """
        df = F.select(F.lit(self).search_sorted(element, side))
        if isinstance(element, (list, Series, pl.Expr, np.ndarray)):
            return df.to_series()
        else:
            return df.item()
