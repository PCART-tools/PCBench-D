    def parse_int(self, radix: int = 2, *, strict: bool = True) -> Expr:
        """
        Parse integers with base radix from strings.

        By default base 2. ParseError/Overflows become Nulls.

        Parameters
        ----------
        radix
            Positive integer which is the base of the string we are parsing.
            Default: 2.

        strict
            Bool, Default=True will raise any ParseError or overflow as ComputeError.
            False silently convert to Null.

        Returns
        -------
        Expr
            Expression of data type :class:`Int32`.

        Examples
        --------
        >>> df = pl.DataFrame({"bin": ["110", "101", "010", "invalid"]})
        >>> df.select(pl.col("bin").str.parse_int(2, strict=False))
        shape: (4, 1)
        ┌──────┐
        │ bin  │
        │ ---  │
        │ i32  │
        ╞══════╡
        │ 6    │
        │ 5    │
        │ 2    │
        │ null │
        └──────┘

        >>> df = pl.DataFrame({"hex": ["fa1e", "ff00", "cafe", None]})
        >>> df.select(pl.col("hex").str.parse_int(16, strict=True))
        shape: (4, 1)
        ┌───────┐
        │ hex   │
        │ ---   │
        │ i32   │
        ╞═══════╡
        │ 64030 │
        │ 65280 │
        │ 51966 │
        │ null  │
        └───────┘

        """
        return wrap_expr(self._pyexpr.str_parse_int(radix, strict))
