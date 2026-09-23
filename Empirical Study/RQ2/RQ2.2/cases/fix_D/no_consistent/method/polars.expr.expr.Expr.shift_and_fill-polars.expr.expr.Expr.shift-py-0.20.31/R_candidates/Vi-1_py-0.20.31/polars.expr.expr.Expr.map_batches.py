    def map_batches(
        self,
        function: Callable[[Series], Series | Any],
        return_dtype: PolarsDataType | None = None,
        *,
        agg_list: bool = False,
        is_elementwise: bool = False,
        returns_scalar: bool = False,
    ) -> Self:
        """
        Apply a custom python function to a whole Series or sequence of Series.

        The output of this custom function is presumed to be either a Series,
        or a NumPy array (in which case it will be automatically converted into
        a Series), or a scalar that will be converted into a Series. If the
        result is a scalar and you want it to stay as a scalar, pass in
        ``returns_scalar=True``. If you want to apply a
        custom function elementwise over single values, see :func:`map_elements`.
        A reasonable use case for `map` functions is transforming the values
        represented by an expression using a third-party library.

        If your function returns a scalar, for example a float, use
        :func:`map_to_scalar` instead.

        Parameters
        ----------
        function
            Lambda/function to apply.
        return_dtype
            Dtype of the output Series.
            If not set, the dtype will be inferred based on the first non-null value
            that is returned by the function.
        is_elementwise
            If set to true this can run in the streaming engine, but may yield
            incorrect results in group-by. Ensure you know what you are doing!
        agg_list
            Aggregate the values of the expression into a list before applying the
            function. This parameter only works in a group-by context.
            The function will be invoked only once on a list of groups, rather than
            once per group.
        returns_scalar
            If the function returns a scalar, by default it will be wrapped in
            a list in the output, since the assumption is that the function
            always returns something Series-like. If you want to keep the
            result as a scalar, set this argument to True.

        Warnings
        --------
        If `return_dtype` is not provided, this may lead to unexpected results.
        We allow this, but it is considered a bug in the user's query.

        See Also
        --------
        map_elements
        replace

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

        In a group-by context, the `agg_list` parameter can improve performance if used
        correctly. The following example has `agg_list` set to `False`, which causes
        the function to be applied once per group. The input of the function is a
        Series of type `Int64`. This is less efficient.

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [0, 1, 0, 1],
        ...         "b": [1, 2, 3, 4],
        ...     }
        ... )
        >>> df.group_by("a").agg(
        ...     pl.col("b").map_batches(lambda x: x + 2, agg_list=False)
        ... )  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌─────┬───────────┐
        │ a   ┆ b         │
        │ --- ┆ ---       │
        │ i64 ┆ list[i64] │
        ╞═════╪═══════════╡
        │ 1   ┆ [4, 6]    │
        │ 0   ┆ [3, 5]    │
        └─────┴───────────┘

        Using `agg_list=True` would be more efficient. In this example, the input of
        the function is a Series of type `List(Int64)`.

        >>> df.group_by("a").agg(
        ...     pl.col("b").map_batches(
        ...         lambda x: x.list.eval(pl.element() + 2), agg_list=True
        ...     )
        ... )  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌─────┬───────────┐
        │ a   ┆ b         │
        │ --- ┆ ---       │
        │ i64 ┆ list[i64] │
        ╞═════╪═══════════╡
        │ 0   ┆ [3, 5]    │
        │ 1   ┆ [4, 6]    │
        └─────┴───────────┘

        Here's an example of a function that returns a scalar, where we want it
        to stay as a scalar:

        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [0, 1, 0, 1],
        ...         "b": [1, 2, 3, 4],
        ...     }
        ... )
        >>> df.group_by("a").agg(
        ...     pl.col("b").map_batches(lambda x: x.max(), returns_scalar=True)
        ... )  # doctest: +IGNORE_RESULT
        shape: (2, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 4   │
        │ 0   ┆ 3   │
        └─────┴─────┘

        """
        if return_dtype is not None:
            return_dtype = py_type_to_dtype(return_dtype)

        return self._from_pyexpr(
            self._pyexpr.map_batches(
                self._map_batches_wrapper(function, return_dtype),
                return_dtype,
                agg_list,
                is_elementwise,
                returns_scalar,
            )
        )
