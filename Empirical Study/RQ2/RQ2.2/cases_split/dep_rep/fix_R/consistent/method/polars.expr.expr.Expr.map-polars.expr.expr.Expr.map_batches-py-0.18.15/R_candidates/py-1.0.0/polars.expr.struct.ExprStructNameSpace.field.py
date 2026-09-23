    def field(self, name: str | list[str], *more_names: str) -> Expr:
        """
        Retrieve one or multiple `Struct` field(s) as a new Series.

        Parameters
        ----------
        name
            Name of the struct field to retrieve.
        *more_names
            Additional struct field names.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "aaa": [1, 2],
        ...         "bbb": ["ab", "cd"],
        ...         "ccc": [True, None],
        ...         "ddd": [[1, 2], [3]],
        ...     }
        ... ).select(pl.struct("aaa", "bbb", "ccc", "ddd").alias("struct_col"))
        >>> df
        shape: (2, 1)
        ┌──────────────────────┐
        │ struct_col           │
        │ ---                  │
        │ struct[4]            │
        ╞══════════════════════╡
        │ {1,"ab",true,[1, 2]} │
        │ {2,"cd",null,[3]}    │
        └──────────────────────┘

        Retrieve struct field(s) as Series:

        >>> df.select(pl.col("struct_col").struct.field("bbb"))
        shape: (2, 1)
        ┌─────┐
        │ bbb │
        │ --- │
        │ str │
        ╞═════╡
        │ ab  │
        │ cd  │
        └─────┘

        >>> df.select(
        ...     pl.col("struct_col").struct.field("bbb"),
        ...     pl.col("struct_col").struct.field("ddd"),
        ... )
        shape: (2, 2)
        ┌─────┬───────────┐
        │ bbb ┆ ddd       │
        │ --- ┆ ---       │
        │ str ┆ list[i64] │
        ╞═════╪═══════════╡
        │ ab  ┆ [1, 2]    │
        │ cd  ┆ [3]       │
        └─────┴───────────┘

        Use wildcard expansion:

        >>> df.select(pl.col("struct_col").struct.field("*"))
        shape: (2, 4)
        ┌─────┬─────┬──────┬───────────┐
        │ aaa ┆ bbb ┆ ccc  ┆ ddd       │
        │ --- ┆ --- ┆ ---  ┆ ---       │
        │ i64 ┆ str ┆ bool ┆ list[i64] │
        ╞═════╪═════╪══════╪═══════════╡
        │ 1   ┆ ab  ┆ true ┆ [1, 2]    │
        │ 2   ┆ cd  ┆ null ┆ [3]       │
        └─────┴─────┴──────┴───────────┘

        Retrieve multiple fields by name:

        >>> df.select(pl.col("struct_col").struct.field("aaa", "bbb"))
        shape: (2, 2)
        ┌─────┬─────┐
        │ aaa ┆ bbb │
        │ --- ┆ --- │
        │ i64 ┆ str │
        ╞═════╪═════╡
        │ 1   ┆ ab  │
        │ 2   ┆ cd  │
        └─────┴─────┘

        Retrieve multiple fields by regex expansion:

        >>> df.select(pl.col("struct_col").struct.field("^a.*|b.*$"))
        shape: (2, 2)
        ┌─────┬─────┐
        │ aaa ┆ bbb │
        │ --- ┆ --- │
        │ i64 ┆ str │
        ╞═════╪═════╡
        │ 1   ┆ ab  │
        │ 2   ┆ cd  │
        └─────┴─────┘

        Notes
        -----
        The `struct` namespace has implemented `__getitem__`
        so you can also access fields by index:

        >>> df.select(pl.col("struct_col").struct[1])
        shape: (2, 1)
        ┌─────┐
        │ bbb │
        │ --- │
        │ str │
        ╞═════╡
        │ ab  │
        │ cd  │
        └─────┘

        """
        if more_names:
            name = [*([name] if isinstance(name, str) else name), *more_names]
        if isinstance(name, list):
            return wrap_expr(self._pyexpr.struct_multiple_fields(name))

        return wrap_expr(self._pyexpr.struct_field_by_name(name))
