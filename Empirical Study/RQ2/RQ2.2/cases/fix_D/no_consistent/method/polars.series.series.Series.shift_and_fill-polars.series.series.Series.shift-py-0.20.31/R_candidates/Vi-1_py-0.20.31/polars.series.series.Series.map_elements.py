    def map_elements(
        self,
        function: Callable[[Any], Any],
        return_dtype: PolarsDataType | None = None,
        *,
        skip_nulls: bool = True,
    ) -> Self:
        """
        Map a custom/user-defined function (UDF) over elements in this Series.

        .. warning::
            This method is much slower than the native expressions API.
            Only use it if you cannot implement your logic otherwise.

            Suppose that the function is: `x ↦ sqrt(x)`:

            - For mapping elements of a series, consider: `s.sqrt()`.
            - For mapping inner elements of lists, consider:
              `s.list.eval(pl.element().sqrt())`.

        If the function returns a different datatype, the return_dtype arg should
        be set, otherwise the method will fail.

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
            Output datatype.
            If not set, the dtype will be inferred based on the first non-null value
            that is returned by the function.
        skip_nulls
            Nulls will be skipped and not passed to the python function.
            This is faster because python can be skipped and because we call
            more specialized functions.

        Warnings
        --------
        If `return_dtype` is not provided, this may lead to unexpected results.
        We allow this, but it is considered a bug in the user's query.

        Notes
        -----
        If your function is expensive and you don't want it to be called more than
        once for a given input, consider applying an `@lru_cache` decorator to it.
        If your data is suitable you may achieve *significant* speedups.

        Examples
        --------
        >>> s = pl.Series("a", [1, 2, 3])
        >>> s.map_elements(lambda x: x + 10, return_dtype=pl.Int64)  # doctest: +SKIP
        shape: (3,)
        Series: 'a' [i64]
        [
                11
                12
                13
        ]

        Returns
        -------
        Series
        """
        from polars._utils.udfs import warn_on_inefficient_map

        if return_dtype is None:
            pl_return_dtype = None
        else:
            pl_return_dtype = py_type_to_dtype(return_dtype)

        warn_on_inefficient_map(function, columns=[self.name], map_target="series")
        return self._from_pyseries(
            self._s.apply_lambda(function, pl_return_dtype, skip_nulls)
        )
