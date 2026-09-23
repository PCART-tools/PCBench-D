    def to_struct(
        self,
        n_field_strategy: ToStructStrategy = "first_non_null",
        fields: Sequence[str] | Callable[[int], str] | None = None,
        upper_bound: int = 0,
    ) -> Expr:
        """
        Convert the Series of type `List` to a Series of type `Struct`.

        Parameters
        ----------
        n_field_strategy : {'first_non_null', 'max_width'}
            Strategy to determine the number of fields of the struct.

            * "first_non_null": set number of fields equal to the length of the
              first non zero-length sublist.
            * "max_width": set number of fields as max length of all sublists.
        fields
            If the name and number of the desired fields is known in advance
            a list of field names can be given, which will be assigned by index.
            Otherwise, to dynamically assign field names, a custom function can be
            used; if neither are set, fields will be `field_0, field_1 .. field_n`.
        upper_bound
            A polars `LazyFrame` needs to know the schema at all times, so the
            caller must provide an upper bound of the number of struct fields that
            will be created; if set incorrectly, subsequent operations may fail.
            (For example, an `all().sum()` expression will look in the current
            schema to determine which columns to select).

            When operating on a `DataFrame`, the schema does not need to be
            tracked or pre-determined, as the result will be eagerly evaluated,
            so you can leave this parameter unset.

        Notes
        -----
        For performance reasons, the length of the first non-null sublist is used
        to determine the number of output fields. If the sublists can be of different
        lengths then `n_field_strategy="max_width"` must be used to obtain the expected
        result.

        Examples
        --------
        Convert list to struct with default field name assignment:

        >>> df = pl.DataFrame({"n": [[0, 1], [0, 1, 2]]})
        >>> df.with_columns(
        ...     struct=pl.col("n").list.to_struct()
        ... )  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌───────────┬───────────┐
        │ n         ┆ struct    │
        │ ---       ┆ ---       │
        │ list[i64] ┆ struct[2] │ # <- struct with 2 fields
        ╞═══════════╪═══════════╡
        │ [0, 1]    ┆ {0,1}     │ # OK
        │ [0, 1, 2] ┆ {0,1}     │ # NOT OK - last value missing
        └───────────┴───────────┘

        As the shorter sublist comes first, we must use the `max_width`
        strategy to force a search for the longest.

        >>> df.with_columns(
        ...     struct=pl.col("n").list.to_struct(n_field_strategy="max_width")
        ... )  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌───────────┬────────────┐
        │ n         ┆ struct     │
        │ ---       ┆ ---        │
        │ list[i64] ┆ struct[3]  │ # <- struct with 3 fields
        ╞═══════════╪════════════╡
        │ [0, 1]    ┆ {0,1,null} │ # OK
        │ [0, 1, 2] ┆ {0,1,2}    │ # OK
        └───────────┴────────────┘

        Convert list to struct with field name assignment by function/index:

        >>> df = pl.DataFrame({"n": [[0, 1], [2, 3]]})
        >>> df.select(pl.col("n").list.to_struct(fields=lambda idx: f"n{idx}")).rows(
        ...     named=True
        ... )
        [{'n': {'n0': 0, 'n1': 1}}, {'n': {'n0': 2, 'n1': 3}}]

        Convert list to struct with field name assignment by index from a list of names:

        >>> df.select(pl.col("n").list.to_struct(fields=["one", "two"])).rows(
        ...     named=True
        ... )
        [{'n': {'one': 0, 'two': 1}}, {'n': {'one': 2, 'two': 3}}]
        """
        if isinstance(fields, Sequence):
            field_names = list(fields)
            pyexpr = self._pyexpr.list_to_struct(n_field_strategy, None, upper_bound)
            return wrap_expr(pyexpr).struct.rename_fields(field_names)
        else:
            pyexpr = self._pyexpr.list_to_struct(n_field_strategy, fields, upper_bound)
            return wrap_expr(pyexpr)
