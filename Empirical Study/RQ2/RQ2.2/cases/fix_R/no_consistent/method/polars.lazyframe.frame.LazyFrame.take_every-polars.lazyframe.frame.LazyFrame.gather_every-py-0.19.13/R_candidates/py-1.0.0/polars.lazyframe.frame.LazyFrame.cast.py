    def cast(
        self,
        dtypes: (
            Mapping[ColumnNameOrSelector | PolarsDataType, PolarsDataType]
            | PolarsDataType
        ),
        *,
        strict: bool = True,
    ) -> LazyFrame:
        """
        Cast LazyFrame column(s) to the specified dtype(s).

        Parameters
        ----------
        dtypes
            Mapping of column names (or selector) to dtypes, or a single dtype
            to which all columns will be cast.
        strict
            Throw an error if a cast could not be done (for instance, due to an
            overflow).

        Examples
        --------
        >>> from datetime import date
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6.0, 7.0, 8.0],
        ...         "ham": [date(2020, 1, 2), date(2021, 3, 4), date(2022, 5, 6)],
        ...     }
        ... )

        Cast specific frame columns to the specified dtypes:

        >>> lf.cast({"foo": pl.Float32, "bar": pl.UInt8}).collect()
        shape: (3, 3)
        ┌─────┬─────┬────────────┐
        │ foo ┆ bar ┆ ham        │
        │ --- ┆ --- ┆ ---        │
        │ f32 ┆ u8  ┆ date       │
        ╞═════╪═════╪════════════╡
        │ 1.0 ┆ 6   ┆ 2020-01-02 │
        │ 2.0 ┆ 7   ┆ 2021-03-04 │
        │ 3.0 ┆ 8   ┆ 2022-05-06 │
        └─────┴─────┴────────────┘

        Cast all frame columns matching one dtype (or dtype group) to another dtype:

        >>> lf.cast({pl.Date: pl.Datetime}).collect()
        shape: (3, 3)
        ┌─────┬─────┬─────────────────────┐
        │ foo ┆ bar ┆ ham                 │
        │ --- ┆ --- ┆ ---                 │
        │ i64 ┆ f64 ┆ datetime[μs]        │
        ╞═════╪═════╪═════════════════════╡
        │ 1   ┆ 6.0 ┆ 2020-01-02 00:00:00 │
        │ 2   ┆ 7.0 ┆ 2021-03-04 00:00:00 │
        │ 3   ┆ 8.0 ┆ 2022-05-06 00:00:00 │
        └─────┴─────┴─────────────────────┘

        Use selectors to define the columns being cast:

        >>> import polars.selectors as cs
        >>> lf.cast({cs.numeric(): pl.UInt32, cs.temporal(): pl.String}).collect()
        shape: (3, 3)
        ┌─────┬─────┬────────────┐
        │ foo ┆ bar ┆ ham        │
        │ --- ┆ --- ┆ ---        │
        │ u32 ┆ u32 ┆ str        │
        ╞═════╪═════╪════════════╡
        │ 1   ┆ 6   ┆ 2020-01-02 │
        │ 2   ┆ 7   ┆ 2021-03-04 │
        │ 3   ┆ 8   ┆ 2022-05-06 │
        └─────┴─────┴────────────┘

        Cast all frame columns to the specified dtype:

        >>> lf.cast(pl.String).collect().to_dict(as_series=False)
        {'foo': ['1', '2', '3'],
         'bar': ['6.0', '7.0', '8.0'],
         'ham': ['2020-01-02', '2021-03-04', '2022-05-06']}
        """
        if not isinstance(dtypes, Mapping):
            return self._from_pyldf(self._ldf.cast_all(dtypes, strict))

        cast_map = {}
        for c, dtype in dtypes.items():
            if (is_polars_dtype(c) or isinstance(c, DataTypeGroup)) or (
                isinstance(c, Collection) and all(is_polars_dtype(x) for x in c)
            ):
                c = by_dtype(c)  # type: ignore[arg-type]

            dtype = parse_into_dtype(dtype)
            cast_map.update(
                {c: dtype}
                if isinstance(c, str)
                else {x: dtype for x in expand_selector(self, c)}  # type: ignore[arg-type]
            )

        return self._from_pyldf(self._ldf.cast(cast_map, strict))
