    def zfill(self, alignment: int) -> Expr:
        """
        Fills the string with zeroes.

        Return a copy of the string left filled with ASCII '0' digits to make a string
        of length width.

        A leading sign prefix ('+'/'-') is handled by inserting the padding after the
        sign character rather than before. The original string is returned if width is
        less than or equal to ``len(s)``.

        Parameters
        ----------
        alignment
            Fill the value up to this length

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "num": [-10, -1, 0, 1, 10, 100, 1000, 10000, 100000, 1000000, None],
        ...     }
        ... )
        >>> df.with_columns(pl.col("num").cast(str).str.zfill(5))
        shape: (11, 1)
        ┌─────────┐
        │ num     │
        │ ---     │
        │ str     │
        ╞═════════╡
        │ -0010   │
        │ -0001   │
        │ 00000   │
        │ 00001   │
        │ …       │
        │ 10000   │
        │ 100000  │
        │ 1000000 │
        │ null    │
        └─────────┘

        """
        return wrap_expr(self._pyexpr.str_zfill(alignment))
