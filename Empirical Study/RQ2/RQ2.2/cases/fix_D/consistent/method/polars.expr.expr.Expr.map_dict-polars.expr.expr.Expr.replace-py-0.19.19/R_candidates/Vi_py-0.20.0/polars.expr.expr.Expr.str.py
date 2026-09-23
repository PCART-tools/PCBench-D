    @property
    def str(self) -> ExprStringNameSpace:
        """
        Create an object namespace of all string related methods.

        See the individual method pages for full details.

        Examples
        --------
        >>> df = pl.DataFrame({"letters": ["a", "b"]})
        >>> df.select(pl.col("letters").str.to_uppercase())
        shape: (2, 1)
        ┌─────────┐
        │ letters │
        │ ---     │
        │ str     │
        ╞═════════╡
        │ A       │
        │ B       │
        └─────────┘

        """
        return ExprStringNameSpace(self)
