    def cast(
        self,
        dtype: PolarsDataType | type[Any],
        *,
        strict: bool = True,
        wrap_numerical: bool = False,
    ) -> Expr:
        r"""
        Cast between data types.

        Parameters
        ----------
        dtype
            DataType to cast to.
        strict
            If True invalid casts generate exceptions instead of `null`\s.
        wrap_numerical
            If True numeric casts wrap overflowing values instead of
            marking the cast as invalid.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3],
        ...         "b": ["4", "5", "6"],
        ...     }
        ... )
        >>> df.with_columns(
        ...     pl.col("a").cast(pl.Float64),
        ...     pl.col("b").cast(pl.Int32),
        ... )
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ f64 ┆ i32 │
        ╞═════╪═════╡
        │ 1.0 ┆ 4   │
        │ 2.0 ┆ 5   │
        │ 3.0 ┆ 6   │
        └─────┴─────┘
        """
        dtype = parse_into_dtype(dtype)
        return self._from_pyexpr(self._pyexpr.cast(dtype, strict, wrap_numerical))
