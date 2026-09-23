    def fill_null(
        self,
        value: Any | None = None,
        strategy: FillNullStrategy | None = None,
        limit: int | None = None,
        *,
        matches_supertype: bool = True,
    ) -> Self:
        """
        Fill null values using the specified value or strategy.

        Parameters
        ----------
        value
            Value used to fill null values.
        strategy : {None, 'forward', 'backward', 'min', 'max', 'mean', 'zero', 'one'}
            Strategy used to fill null values.
        limit
            Number of consecutive null values to fill when using the 'forward' or
            'backward' strategy.
        matches_supertype
            Fill all matching supertypes of the fill `value` literal.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": [1, 2, None, 4],
        ...         "b": [0.5, 4, None, 13],
        ...     }
        ... )
        >>> lf.fill_null(99).collect()
        shape: (4, 2)
        ┌─────┬──────┐
        │ a   ┆ b    │
        │ --- ┆ ---  │
        │ i64 ┆ f64  │
        ╞═════╪══════╡
        │ 1   ┆ 0.5  │
        │ 2   ┆ 4.0  │
        │ 99  ┆ 99.0 │
        │ 4   ┆ 13.0 │
        └─────┴──────┘
        >>> lf.fill_null(strategy="forward").collect()
        shape: (4, 2)
        ┌─────┬──────┐
        │ a   ┆ b    │
        │ --- ┆ ---  │
        │ i64 ┆ f64  │
        ╞═════╪══════╡
        │ 1   ┆ 0.5  │
        │ 2   ┆ 4.0  │
        │ 2   ┆ 4.0  │
        │ 4   ┆ 13.0 │
        └─────┴──────┘

        >>> lf.fill_null(strategy="max").collect()
        shape: (4, 2)
        ┌─────┬──────┐
        │ a   ┆ b    │
        │ --- ┆ ---  │
        │ i64 ┆ f64  │
        ╞═════╪══════╡
        │ 1   ┆ 0.5  │
        │ 2   ┆ 4.0  │
        │ 4   ┆ 13.0 │
        │ 4   ┆ 13.0 │
        └─────┴──────┘

        >>> lf.fill_null(strategy="zero").collect()
        shape: (4, 2)
        ┌─────┬──────┐
        │ a   ┆ b    │
        │ --- ┆ ---  │
        │ i64 ┆ f64  │
        ╞═════╪══════╡
        │ 1   ┆ 0.5  │
        │ 2   ┆ 4.0  │
        │ 0   ┆ 0.0  │
        │ 4   ┆ 13.0 │
        └─────┴──────┘

        """
        dtypes: Sequence[PolarsDataType]

        if value is not None:

            def infer_dtype(value: Any) -> PolarsDataType:
                return next(iter(self.select(value).schema.values()))

            if isinstance(value, pl.Expr):
                dtypes = [infer_dtype(value)]
            elif isinstance(value, bool):
                dtypes = [Boolean]
            elif matches_supertype and isinstance(value, (int, float)):
                dtypes = [
                    Int8,
                    Int16,
                    Int32,
                    Int64,
                    UInt8,
                    UInt16,
                    UInt32,
                    UInt64,
                    Float32,
                    Float64,
                ]
            elif isinstance(value, int):
                dtypes = [Int64]
            elif isinstance(value, float):
                dtypes = [Float64]
            elif isinstance(value, datetime):
                dtypes = [Datetime] + [Datetime(u) for u in DTYPE_TEMPORAL_UNITS]
            elif isinstance(value, timedelta):
                dtypes = [Duration] + [Duration(u) for u in DTYPE_TEMPORAL_UNITS]
            elif isinstance(value, date):
                dtypes = [Date]
            elif isinstance(value, time):
                dtypes = [Time]
            elif isinstance(value, str):
                dtypes = [Utf8, Categorical]
            else:
                # fallback; anything not explicitly handled above
                dtypes = [infer_dtype(F.lit(value))]

            return self.with_columns(F.col(dtypes).fill_null(value, strategy, limit))

        return self.select(F.all().fill_null(value, strategy, limit))
