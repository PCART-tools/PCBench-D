    def drop_nans(self) -> Expr:
        """
        Drop all floating point NaN values.

        The original order of the remaining elements is preserved.

        See Also
        --------
        drop_nulls

        Notes
        -----
        A NaN value is not the same as a null value.
        To drop null values, use :func:`drop_nulls`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": [1.0, None, 3.0, float("nan")]})
        >>> df.select(pl.col("a").drop_nans())
        shape: (3, 1)
        ┌──────┐
        │ a    │
        │ ---  │
        │ f64  │
        ╞══════╡
        │ 1.0  │
        │ null │
        │ 3.0  │
        └──────┘
        """
        return self._from_pyexpr(self._pyexpr.drop_nans())
