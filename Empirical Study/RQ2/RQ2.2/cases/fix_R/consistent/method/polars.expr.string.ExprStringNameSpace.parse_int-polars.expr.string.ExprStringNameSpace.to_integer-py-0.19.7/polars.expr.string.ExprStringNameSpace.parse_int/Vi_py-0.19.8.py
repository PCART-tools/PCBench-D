    def parse_int(self, radix: int | None = None, *, strict: bool = True) -> Expr:
        """
        Parse integers with base radix from strings.

        ParseError/Overflows become Nulls.

        Parameters
        ----------
        radix
            Positive integer which is the base of the string we are parsing.
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
        if radix is None:
            issue_deprecation_warning(
                "The default value for the `radix` parameter of `parse_int` will be removed in a future version."
                " Call `parse_int(radix=2)` to keep current behavior and silence this warning.",
                version="0.19.8",
            )
            radix = 2

        return wrap_expr(self._pyexpr.str_parse_int(radix, strict))
