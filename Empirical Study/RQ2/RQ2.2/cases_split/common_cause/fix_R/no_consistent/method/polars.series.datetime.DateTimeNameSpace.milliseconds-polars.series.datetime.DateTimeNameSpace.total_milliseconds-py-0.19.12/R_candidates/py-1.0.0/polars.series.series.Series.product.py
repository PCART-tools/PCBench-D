    def product(self) -> int | float:
        """
        Reduce this Series to the product value.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.product()
        6
        """
        return self._s.product()
