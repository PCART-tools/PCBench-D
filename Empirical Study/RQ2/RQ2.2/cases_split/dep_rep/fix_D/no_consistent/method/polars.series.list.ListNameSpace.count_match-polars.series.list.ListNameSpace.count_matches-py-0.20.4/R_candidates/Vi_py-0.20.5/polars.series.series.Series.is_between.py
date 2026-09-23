    def is_between(
        self,
        lower_bound: IntoExpr,
        upper_bound: IntoExpr,
        closed: ClosedInterval = "both",
    ) -> Series:
        """
        Get a boolean mask of the values that are between the given lower/upper bounds.

        Parameters
        ----------
        lower_bound
            Lower bound value. Accepts expression input. Non-expression inputs
            (including strings) are parsed as literals.
        upper_bound
            Upper bound value. Accepts expression input. Non-expression inputs
            (including strings) are parsed as literals.
        closed : {'both', 'left', 'right', 'none'}
            Define which sides of the interval are closed (inclusive).

        Examples
        --------
        >>> s = pl.Series("num", [1, 2, 3, 4, 5])
        >>> s.is_between(2, 4)
        shape: (5,)
        Series: 'num' [bool]
        [
            false
            true
            true
            true
            false
        ]

        Use the `closed` argument to include or exclude the values at the bounds:

        >>> s.is_between(2, 4, closed="left")
        shape: (5,)
        Series: 'num' [bool]
        [
            false
            true
            true
            false
            false
        ]

        You can also use strings as well as numeric/temporal values:

        >>> s = pl.Series("s", ["a", "b", "c", "d", "e"])
        >>> s.is_between("b", "d", closed="both")
        shape: (5,)
        Series: 's' [bool]
        [
            false
            true
            true
            true
            false
        ]
        """
        if closed == "none":
            out = (self > lower_bound) & (self < upper_bound)
        elif closed == "both":
            out = (self >= lower_bound) & (self <= upper_bound)
        elif closed == "right":
            out = (self > lower_bound) & (self <= upper_bound)
        elif closed == "left":
            out = (self >= lower_bound) & (self < upper_bound)

        if isinstance(out, pl.Expr):
            out = F.select(out).to_series()

        return out
