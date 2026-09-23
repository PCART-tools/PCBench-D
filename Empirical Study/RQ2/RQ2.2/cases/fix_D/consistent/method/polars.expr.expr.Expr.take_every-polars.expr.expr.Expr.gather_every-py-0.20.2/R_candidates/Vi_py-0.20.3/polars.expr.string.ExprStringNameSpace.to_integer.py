    def to_integer(self, *, base: int = 10, strict: bool = True) -> Expr:
        """
        Convert an String column into an Int64 column with base radix.

        Parameters
        ----------
        base
            Positive integer which is the base of the string we are parsing.
            Default: 10.
        strict
            Bool, Default=True will raise any ParseError or overflow as ComputeError.
            False silently convert to Null.

        Returns
        -------
        Expr
            Expression of data type :class:`Int64`.

        Examples
        --------
        >>> df = pl.DataFrame({"bin": ["110", "101", "010", "invalid"]})
        >>> df.with_columns(parsed=pl.col("bin").str.to_integer(base=2, strict=False))
        shape: (4, 2)
        ┌─────────┬────────┐
        │ bin     ┆ parsed │
        │ ---     ┆ ---    │
        │ str     ┆ i64    │
        ╞═════════╪════════╡
        │ 110     ┆ 6      │
        │ 101     ┆ 5      │
        │ 010     ┆ 2      │
        │ invalid ┆ null   │
        └─────────┴────────┘

        >>> df = pl.DataFrame({"hex": ["fa1e", "ff00", "cafe", None]})
        >>> df.with_columns(parsed=pl.col("hex").str.to_integer(base=16, strict=True))
        shape: (4, 2)
        ┌──────┬────────┐
        │ hex  ┆ parsed │
        │ ---  ┆ ---    │
        │ str  ┆ i64    │
        ╞══════╪════════╡
        │ fa1e ┆ 64030  │
        │ ff00 ┆ 65280  │
        │ cafe ┆ 51966  │
        │ null ┆ null   │
        └──────┴────────┘

        """
        return wrap_expr(self._pyexpr.str_to_integer(base, strict))
