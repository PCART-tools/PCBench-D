    def drop_nulls(self) -> Self:
        """
        Drop all null values.

        The original order of the remaining elements is preserved.

        See Also
        --------
        drop_nans

        Notes
        -----
        A null value is not the same as a NaN value.
        To drop NaN values, use :func:`drop_nans`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1.0, None, 3.0, float("nan")]})
        >>> df.select(pl.col("a").drop_nulls())
        shape: (3, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ f64 │
        ╞═════╡
        │ 1.0 │
        │ 3.0 │
        │ NaN │
        └─────┘

        """
        return self._from_pyexpr(self._pyexpr.drop_nulls())
