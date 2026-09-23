    def pipe(
        self,
        function: Callable[Concatenate[Expr, P], T],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        r'''
        Offers a structured way to apply a sequence of user-defined functions (UDFs).

        Parameters
        ----------
        function
            Callable; will receive the expression as the first parameter,
            followed by any given args/kwargs.
        *args
            Arguments to pass to the UDF.
        **kwargs
            Keyword arguments to pass to the UDF.

        Examples
        --------
        >>> def extract_number(expr: pl.Expr) -> pl.Expr:
        ...     """Extract the digits from a string."""
        ...     return expr.str.extract(r"\d+", 0).cast(pl.Int64)
        >>>
        >>> def scale_negative_even(expr: pl.Expr, *, n: int = 1) -> pl.Expr:
        ...     """Set even numbers negative, and scale by a user-supplied value."""
        ...     expr = pl.when(expr % 2 == 0).then(-expr).otherwise(expr)
        ...     return expr * n
        >>>
        >>> df = pl.DataFrame({"val": ["a: 1", "b: 2", "c: 3", "d: 4"]})
        >>> df.with_columns(
        ...     udfs=(
        ...         pl.col("val").pipe(extract_number).pipe(scale_negative_even, n=5)
        ...     ),
        ... )
        shape: (4, 2)
        ┌──────┬──────┐
        │ val  ┆ udfs │
        │ ---  ┆ ---  │
        │ str  ┆ i64  │
        ╞══════╪══════╡
        │ a: 1 ┆ 5    │
        │ b: 2 ┆ -10  │
        │ c: 3 ┆ 15   │
        │ d: 4 ┆ -20  │
        └──────┴──────┘

        '''
        return function(self, *args, **kwargs)
