    def get(self, index: int | Expr | str) -> Expr:
        """
        Get the value by index in the sublists.

        So index `0` would return the first item of every sublist
        and index `-1` would return the last item of every sublist
        if an index is out of bounds, it will return a `None`.

        Parameters
        ----------
        index
            Index to return per sublist

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [[3, 2, 1], [], [1, 2]]})
        >>> df.select(pl.col("foo").list.get(0))
        shape: (3, 1)
        ┌──────┐
        │ foo  │
        │ ---  │
        │ i64  │
        ╞══════╡
        │ 3    │
        │ null │
        │ 1    │
        └──────┘

        """
        index = parse_as_expression(index)
        return wrap_expr(self._pyexpr.list_get(index))
