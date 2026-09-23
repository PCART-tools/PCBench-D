    def to_decimal(
        self,
        inference_length: int = 100,
    ) -> Expr:
        """
        Convert a Utf8 column into a Decimal column.

        This method infers the needed parameters ``precision`` and ``scale``.

        Parameters
        ----------
        inference_length
            Number of elements to parse to determine the `precision` and `scale`.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "numbers": [
        ...             "40.12",
        ...             "3420.13",
        ...             "120134.19",
        ...             "3212.98",
        ...             "12.90",
        ...             "143.09",
        ...             "143.9",
        ...         ]
        ...     }
        ... )
        >>> df.select(pl.col("numbers").str.to_decimal())
        shape: (7, 1)
        ┌────────────┐
        │ numbers    │
        │ ---        │
        │ decimal[2] │
        ╞════════════╡
        │ 40.12      │
        │ 3420.13    │
        │ 120134.19  │
        │ 3212.98    │
        │ 12.9       │
        │ 143.09     │
        │ 143.9      │
        └────────────┘

        """
        return wrap_expr(self._pyexpr.str_to_decimal(inference_length))
