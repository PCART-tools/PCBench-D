    def rename_fields(self, names: Sequence[str]) -> Expr:
        """
        Rename the fields of the struct.

        Parameters
        ----------
        names
            New names, given in the same order as the struct's fields.

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

        >>> df.unnest("struct_col")
        shape: (2, 4)
        ┌─────┬─────┬──────┬───────────┐
        │ aaa ┆ bbb ┆ ccc  ┆ ddd       │
        │ --- ┆ --- ┆ ---  ┆ ---       │
        │ i64 ┆ str ┆ bool ┆ list[i64] │
        ╞═════╪═════╪══════╪═══════════╡
        │ 1   ┆ ab  ┆ true ┆ [1, 2]    │
        │ 2   ┆ cd  ┆ null ┆ [3]       │
        └─────┴─────┴──────┴───────────┘

        Rename fields:

        >>> df = df.select(
        ...     pl.col("struct_col").struct.rename_fields(["www", "xxx", "yyy", "zzz"])
        ... )
        >>> df.unnest("struct_col")
        shape: (2, 4)
        ┌─────┬─────┬──────┬───────────┐
        │ www ┆ xxx ┆ yyy  ┆ zzz       │
        │ --- ┆ --- ┆ ---  ┆ ---       │
        │ i64 ┆ str ┆ bool ┆ list[i64] │
        ╞═════╪═════╪══════╪═══════════╡
        │ 1   ┆ ab  ┆ true ┆ [1, 2]    │
        │ 2   ┆ cd  ┆ null ┆ [3]       │
        └─────┴─────┴──────┴───────────┘

        Following a rename, the previous field names (obviously) cannot be referenced:

        >>> df.select(pl.col("struct_col").struct.field("aaa"))  # doctest: +SKIP
        StructFieldNotFoundError: aaa
        """
        return wrap_expr(self._pyexpr.struct_rename_fields(names))
