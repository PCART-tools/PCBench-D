    @deprecate_renamed_parameter("drop_nulls", "ignore_nulls", version="0.19.0")
    def all(self, *, ignore_nulls: bool = True) -> Self:
        """
        Return whether all values in the column are `True`.

        Only works on columns of data type :class:`Boolean`.

        .. note::
            This method is not to be confused with the function :func:`polars.all`,
            which can be used to select all columns.

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
        ...         "a": [True, True],
        ...         "b": [False, True],
        ...         "c": [None, True],
        ...     }
        ... )
        >>> df.select(pl.col("*").all())
        shape: (1, 3)
        ┌──────┬───────┬──────┐
        │ a    ┆ b     ┆ c    │
        │ ---  ┆ ---   ┆ ---  │
        │ bool ┆ bool  ┆ bool │
        ╞══════╪═══════╪══════╡
        │ true ┆ false ┆ true │
        └──────┴───────┴──────┘

        Enable Kleene logic by setting `ignore_nulls=False`.

        >>> df.select(pl.col("*").all(ignore_nulls=False))
        shape: (1, 3)
        ┌──────┬───────┬──────┐
        │ a    ┆ b     ┆ c    │
        │ ---  ┆ ---   ┆ ---  │
        │ bool ┆ bool  ┆ bool │
        ╞══════╪═══════╪══════╡
        │ true ┆ false ┆ null │
        └──────┴───────┴──────┘
        """
        return self._from_pyexpr(self._pyexpr.all(ignore_nulls))
