    def neg(self) -> Self:
        """
        Method equivalent of unary minus operator `-expr`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [-1, 0, 2, None]})
        >>> df.with_columns(pl.col("a").neg())
        shape: (4, 1)
        ┌──────┐
        │ a    │
        │ ---  │
        │ i64  │
        ╞══════╡
        │ 1    │
        │ 0    │
        │ -2   │
        │ null │
        └──────┘
        """
        return self.__neg__()
