    def map_rows(
        self,
        function: Callable[[tuple[Any, ...]], Any],
        return_dtype: PolarsDataType | None = None,
        *,
        inference_size: int = 256,
    ) -> DataFrame:
        """
        Apply a custom/user-defined function (UDF) over the rows of the DataFrame.

        .. warning::
            This method is much slower than the native expressions API.
            Only use it if you cannot implement your logic otherwise.

        The UDF will receive each row as a tuple of values: `udf(row)`.

        Implementing logic using a Python function is almost always *significantly*
        slower and more memory intensive than implementing the same logic using
        the native expression API because:

        - The native expression engine runs in Rust; UDFs run in Python.
        - Use of Python UDFs forces the DataFrame to be materialized in memory.
        - Polars-native expressions can be parallelised (UDFs typically cannot).
        - Polars-native expressions can be logically optimised (UDFs cannot).

        Wherever possible you should strongly prefer the native expression API
        to achieve the best performance.

        Parameters
        ----------
        function
            Custom function or lambda.
        return_dtype
            Output type of the operation. If none given, Polars tries to infer the type.
        inference_size
            Only used in the case when the custom function returns rows.
            This uses the first `n` rows to determine the output schema.

        Notes
        -----
        * The frame-level `map_rows` cannot track column names (as the UDF is a
          black-box that may arbitrarily drop, rearrange, transform, or add new
          columns); if you want to apply a UDF such that column names are preserved,
          you should use the expression-level `map_elements` syntax instead.

        * If your function is expensive and you don't want it to be called more than
          once for a given input, consider applying an `@lru_cache` decorator to it.
          If your data is suitable you may achieve *significant* speedups.

        Examples
        --------
        >>> df = pl.DataFrame({"foo": [1, 2, 3], "bar": [-1, 5, 8]})

        Return a DataFrame by mapping each row to a tuple:

        >>> df.map_rows(lambda t: (t[0] * 2, t[1] * 3))
        shape: (3, 2)
        ┌──────────┬──────────┐
        │ column_0 ┆ column_1 │
        │ ---      ┆ ---      │
        │ i64      ┆ i64      │
        ╞══════════╪══════════╡
        │ 2        ┆ -3       │
        │ 4        ┆ 15       │
        │ 6        ┆ 24       │
        └──────────┴──────────┘

        However, it is much better to implement this with a native expression:

        >>> df.select(
        ...     pl.col("foo") * 2,
        ...     pl.col("bar") * 3,
        ... )  # doctest: +IGNORE_RESULT

        Return a DataFrame with a single column by mapping each row to a scalar:

        >>> df.map_rows(lambda t: (t[0] * 2 + t[1]))  # doctest: +SKIP
        shape: (3, 1)
        ┌───────┐
        │ apply │
        │ ---   │
        │ i64   │
        ╞═══════╡
        │ 1     │
        │ 9     │
        │ 14    │
        └───────┘

        In this case it is better to use the following native expression:

        >>> df.select(pl.col("foo") * 2 + pl.col("bar"))  # doctest: +IGNORE_RESULT
        """
        # TODO: Enable warning for inefficient map
        # from polars._utils.udfs import warn_on_inefficient_map
        # warn_on_inefficient_map(function, columns=self.columns, map_target="frame)

        out, is_df = self._df.map_rows(function, return_dtype, inference_size)
        if is_df:
            return self._from_pydf(out)
        else:
            return wrap_s(out).to_frame()
