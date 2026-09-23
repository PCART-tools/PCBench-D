    def to_struct(
        self, fields: Sequence[str] | Callable[[int], str] | None = None
    ) -> Expr:
        """
        Convert the Series of type `Array` to a Series of type `Struct`.

        Parameters
        ----------
        fields
            If the name and number of the desired fields is known in advance
            a list of field names can be given, which will be assigned by index.
            Otherwise, to dynamically assign field names, a custom function can be
            used; if neither are set, fields will be `field_0, field_1 .. field_n`.

        Examples
        --------
        Convert array to struct with default field name assignment:

        >>> df = pl.DataFrame(
        ...     {"n": [[0, 1, 2], [3, 4, 5]]}, schema={"n": pl.Array(pl.Int8, 3)}
        ... )
        >>> df.with_columns(struct=pl.col("n").arr.to_struct())
        shape: (2, 2)
        ┌──────────────┬───────────┐
        │ n            ┆ struct    │
        │ ---          ┆ ---       │
        │ array[i8, 3] ┆ struct[3] │
        ╞══════════════╪═══════════╡
        │ [0, 1, 2]    ┆ {0,1,2}   │
        │ [3, 4, 5]    ┆ {3,4,5}   │
        └──────────────┴───────────┘

        Convert array to struct with field name assignment by function/index:

        >>> df = pl.DataFrame(
        ...     {"n": [[0, 1, 2], [3, 4, 5]]}, schema={"n": pl.Array(pl.Int8, 3)}
        ... )
        >>> df.select(pl.col("n").arr.to_struct(fields=lambda idx: f"n{idx}")).rows(
        ...     named=True
        ... )
        [{'n': {'n0': 0, 'n1': 1, 'n2': 2}}, {'n': {'n0': 3, 'n1': 4, 'n2': 5}}]

        Convert array to struct with field name assignment by
        index from a list of names:

        >>> df.select(pl.col("n").arr.to_struct(fields=["c1", "c2", "c3"])).rows(
        ...     named=True
        ... )
        [{'n': {'c1': 0, 'c2': 1, 'c3': 2}}, {'n': {'c1': 3, 'c2': 4, 'c3': 5}}]
        """
        if isinstance(fields, Sequence):
            field_names = list(fields)
            pyexpr = self._pyexpr.arr_to_struct(None)
            return wrap_expr(pyexpr).struct.rename_fields(field_names)
        else:
            pyexpr = self._pyexpr.arr_to_struct(fields)
            return wrap_expr(pyexpr)
