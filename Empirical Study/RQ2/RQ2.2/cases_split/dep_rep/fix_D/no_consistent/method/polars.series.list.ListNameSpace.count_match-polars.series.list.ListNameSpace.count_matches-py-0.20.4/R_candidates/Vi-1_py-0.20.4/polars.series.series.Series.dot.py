    def dot(self, other: Series | ArrayLike) -> float | None:
        """
        Compute the dot/inner product between two Series.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s2 = pl.Series("b", [4.0, 5.0, 6.0])
        >>> s.dot(s2)
        32.0

        Parameters
        ----------
        other
            Series (or array) to compute dot product with.
        """
        if not isinstance(other, Series):
            other = Series(other)
        if len(self) != len(other):
            n, m = len(self), len(other)
            msg = f"Series length mismatch: expected {n!r}, found {m!r}"
            raise ShapeError(msg)
        return self._s.dot(other._s)
