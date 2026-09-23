    def last(self) -> Expr:
        """
        Get the last value of the sublists.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [[3, 2, 1], [], [1, 2]]})
        >>> df.select(pl.col("foo").list.last())
        shape: (3, 1)
        ┌──────┐
        │ foo  │
        │ ---  │
        │ i64  │
        ╞══════╡
        │ 1    │
        │ null │
        │ 2    │
        └──────┘

        """
        return self.get(-1)
