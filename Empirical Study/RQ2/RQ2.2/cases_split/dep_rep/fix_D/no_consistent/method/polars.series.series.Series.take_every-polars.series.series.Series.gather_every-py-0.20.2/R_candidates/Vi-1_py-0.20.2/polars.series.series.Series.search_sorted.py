    def search_sorted(
        self,
        element: int | float | Series | np.ndarray[Any, Any] | list[int] | list[float],
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

        """
        if isinstance(element, (int, float)):
            return F.select(F.lit(self).search_sorted(element, side)).item()
        element = Series(element)
        return F.select(F.lit(self).search_sorted(element, side)).to_series()
