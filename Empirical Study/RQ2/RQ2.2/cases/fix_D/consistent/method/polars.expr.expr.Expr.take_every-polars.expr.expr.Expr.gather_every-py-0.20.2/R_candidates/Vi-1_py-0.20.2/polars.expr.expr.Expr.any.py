    @deprecate_renamed_parameter("drop_nulls", "ignore_nulls", version="0.19.0")
    def any(self, *, ignore_nulls: bool = True) -> Self:
        """
        Return whether any of the values in the column are `True`.

        Only works on columns of data type :class:`Boolean`.

        Parameters
        ----------
        ignore_nulls
            Ignore null values (default).

            If set to `False`, `Kleene logic`_ is used to deal with nulls:
            if the column contains any null values and no `True` values,
            the output is null.

            .. _Kleene logic: https://en.wikipedia.org/wiki/Three-valued_logic

        Returns
        -------
        Expr
            Expression of data type :class:`Boolean`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [True, False],
        ...         "b": [False, False],
        ...         "c": [None, False],
        ...     }
        ... )
        >>> df.select(pl.col("*").any())
        shape: (1, 3)
        ┌──────┬───────┬───────┐
        │ a    ┆ b     ┆ c     │
        │ ---  ┆ ---   ┆ ---   │
        │ bool ┆ bool  ┆ bool  │
        ╞══════╪═══════╪═══════╡
        │ true ┆ false ┆ false │
        └──────┴───────┴───────┘

        Enable Kleene logic by setting `ignore_nulls=False`.

        >>> df.select(pl.col("*").any(ignore_nulls=False))
        shape: (1, 3)
        ┌──────┬───────┬──────┐
        │ a    ┆ b     ┆ c    │
        │ ---  ┆ ---   ┆ ---  │
        │ bool ┆ bool  ┆ bool │
        ╞══════╪═══════╪══════╡
        │ true ┆ false ┆ null │
        └──────┴───────┴──────┘

        """
        return self._from_pyexpr(self._pyexpr.any(ignore_nulls))
