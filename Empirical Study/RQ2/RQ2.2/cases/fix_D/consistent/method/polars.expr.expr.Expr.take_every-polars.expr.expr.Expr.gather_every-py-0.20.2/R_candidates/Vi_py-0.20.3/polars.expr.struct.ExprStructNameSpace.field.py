    def field(self, name: str) -> Expr:
        """
        Retrieve a `Struct` field as a new Series.

        Parameters
        ----------
        name
            Name of the struct field to retrieve.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "aaa": [1, 2],
        ...         "bbb": ["ab", "cd"],
        ...         "ccc": [True, None],
        ...         "ddd": [[1, 2], [3]],
        ...     }
        ... ).select(pl.struct(["aaa", "bbb", "ccc", "ddd"]).alias("struct_col"))
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

        """
        return wrap_expr(self._pyexpr.struct_field_by_name(name))
