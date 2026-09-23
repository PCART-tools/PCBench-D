    def to_struct(
        self,
        n_field_strategy: ToStructStrategy = "first_non_null",
        fields: Sequence[str] | Callable[[int], str] | None = None,
        upper_bound: int = 0,
    ) -> Expr:
        """
        Convert the series of type ``List`` to a series of type ``Struct``.

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
            A polars ``LazyFrame`` needs to know the schema at all times, so the
            caller must provide an upper bound of the number of struct fields that
            will be created; if set incorrectly, subsequent operations may fail.
            (For example, an ``all().sum()`` expression will look in the current
            schema to determine which columns to select).

            When operating on a ``DataFrame``, the schema does not need to be
            tracked or pre-determined, as the result will be eagerly evaluated,
            so you can leave this parameter unset.

        Examples
        --------
        Convert list to struct with default field name assignment:

        >>> df = pl.DataFrame({"n": [[0, 1, 2], [0, 1]]})
        >>> df.select(pl.col("n").list.to_struct())
        shape: (2, 1)
        ┌────────────┐
        │ n          │
        │ ---        │
        │ struct[3]  │
        ╞════════════╡
        │ {0,1,2}    │
        │ {0,1,null} │
        └────────────┘

        Convert list to struct with field name assignment by function/index:

        >>> df.select(pl.col("n").list.to_struct(fields=lambda idx: f"n{idx}")).rows(
        ...     named=True
        ... )
        [{'n': {'n0': 0, 'n1': 1, 'n2': 2}}, {'n': {'n0': 0, 'n1': 1, 'n2': None}}]

        Convert list to struct with field name assignment by index from a list of names:

        >>> df.select(pl.col("n").list.to_struct(fields=["one", "two", "three"])).rows(
        ...     named=True
        ... )
        [{'n': {'one': 0, 'two': 1, 'three': 2}},
        {'n': {'one': 0, 'two': 1, 'three': None}}]

        """
        if isinstance(fields, Sequence):
            field_names = list(fields)

            def fields(idx: int) -> str:
                return field_names[idx]

        return wrap_expr(
            self._pyexpr.list_to_struct(n_field_strategy, fields, upper_bound)
        )
