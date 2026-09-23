    def map_batches(
        self,
        function: Callable[[Series], Series | Any],
        return_dtype: PolarsDataType | None = None,
        *,
        agg_list: bool = False,
    ) -> Self:
        """
        Apply a custom python function to a whole Series or sequence of Series.

        The output of this custom function must be a Series. If you want to apply a
        custom function elementwise over single values, see :func:`map_elements`.
        A reasonable use case for ``map`` functions is transforming the values
        represented by an expression using a third-party library.

        Read more in `the book
        <https://pola-rs.github.io/polars/user-guide/expressions/user-defined-functions>`_.

        Parameters
        ----------
        function
            Lambda/function to apply.
        return_dtype
            Dtype of the output Series.
        agg_list
            Aggregate list.

        Notes
        -----
        If you are looking to map a function over a window function or groupby context,
        refer to func:`map_elements` instead.

        Warnings
        --------
        If ``return_dtype`` is not provided, this may lead to unexpected results.
        We allow this, but it is considered a bug in the user's query.

        See Also
        --------
        map_dict
        map_elements

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "sine": [0.0, 1.0, 0.0, -1.0],
        ...         "cosine": [1.0, 0.0, -1.0, 0.0],
        ...     }
        ... )
        >>> df.select(pl.all().map_batches(lambda x: x.to_numpy().argmax()))
        shape: (1, 2)
        ┌──────┬────────┐
        │ sine ┆ cosine │
        │ ---  ┆ ---    │
        │ i64  ┆ i64    │
        ╞══════╪════════╡
        │ 1    ┆ 0      │
        └──────┴────────┘

        """
        if return_dtype is not None:
            return_dtype = py_type_to_dtype(return_dtype)
        return self._from_pyexpr(
            self._pyexpr.map_batches(function, return_dtype, agg_list)
        )
