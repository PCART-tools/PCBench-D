    def take(
        self, indices: int | list[int] | Expr | Series | np.ndarray[Any, Any]
    ) -> Self:
        """
        Take values by index.

        Parameters
        ----------
        indices
            An expression that leads to a UInt32 dtyped Series.

        Returns
        -------
        Expr
            Expression of the same data type.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "group": [
        ...             "one",
        ...             "one",
        ...             "one",
        ...             "two",
        ...             "two",
        ...             "two",
        ...         ],
        ...         "value": [1, 98, 2, 3, 99, 4],
        ...     }
        ... )
        >>> df.group_by("group", maintain_order=True).agg(pl.col("value").take(1))
        shape: (2, 2)
        ┌───────┬───────┐
        │ group ┆ value │
        │ ---   ┆ ---   │
        │ str   ┆ i64   │
        ╞═══════╪═══════╡
        │ one   ┆ 98    │
        │ two   ┆ 99    │
        └───────┴───────┘

        """
        if isinstance(indices, list) or (
            _check_for_numpy(indices) and isinstance(indices, np.ndarray)
        ):
            indices_lit = F.lit(pl.Series("", indices, dtype=UInt32))._pyexpr
        else:
            indices_lit = parse_as_expression(indices)  # type: ignore[arg-type]
        return self._from_pyexpr(self._pyexpr.take(indices_lit))
