    def ne_missing(self, other: Any) -> Series | Expr:
        """
        Method equivalent of equality operator `series != other` where `None == None`.

        This differs from the standard `ne` where null values are propagated.

        Parameters
        ----------
        other
            A literal or expression value to compare with.

        See Also
        --------
        eq_missing
        ne

        Examples
        --------
        >>> s1 = pl.Series("a", [333, 200, None])
        >>> s2 = pl.Series("a", [100, 200, None])
        >>> s1.ne(s2)
        shape: (3,)
        Series: 'a' [bool]
        [
            true
            false
            null
        ]
        >>> s1.ne_missing(s2)
        shape: (3,)
        Series: 'a' [bool]
        [
            true
            false
            false
        ]
        """
        if isinstance(other, pl.Expr):
            return F.lit(self).ne_missing(other)
        return self.to_frame().select(F.col(self.name).ne_missing(other)).to_series()
