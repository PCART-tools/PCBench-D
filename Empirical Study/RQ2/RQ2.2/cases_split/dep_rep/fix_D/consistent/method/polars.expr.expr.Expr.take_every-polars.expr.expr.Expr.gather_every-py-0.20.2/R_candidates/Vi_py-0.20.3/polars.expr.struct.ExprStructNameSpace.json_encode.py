    def json_encode(self) -> Expr:
        """
        Convert this struct to a string column with json values.

        Examples
        --------
        >>> pl.DataFrame(
        ...     {"a": [{"a": [1, 2], "b": [45]}, {"a": [9, 1, 3], "b": None}]}
        ... ).with_columns(pl.col("a").struct.json_encode().alias("encoded"))
        shape: (2, 2)
        ┌──────────────────┬────────────────────────┐
        │ a                ┆ encoded                │
        │ ---              ┆ ---                    │
        │ struct[2]        ┆ str                    │
        ╞══════════════════╪════════════════════════╡
        │ {[1, 2],[45]}    ┆ {"a":[1,2],"b":[45]}   │
        │ {[9, 1, 3],null} ┆ {"a":[9,1,3],"b":null} │
        └──────────────────┴────────────────────────┘

        """
        return wrap_expr(self._pyexpr.struct_json_encode())
