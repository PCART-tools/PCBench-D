    def apply(
        self,
        function: Callable[[Series], Series] | Callable[[Any], Any],
        return_dtype: PolarsDataType | None = None,
        *,
        skip_nulls: bool = True,
        pass_name: bool = False,
        strategy: ApplyStrategy = "thread_local",
    ) -> Self:
        """
        Apply a custom/user-defined function (UDF) in a GroupBy or Projection context.

        .. warning::
            This method is much slower than the native expressions API.
            Only use it if you cannot implement your logic otherwise.

        Depending on the context it has the following behavior:

        * Selection
            Expects `f` to be of type Callable[[Any], Any].
            Applies a python function over each individual value in the column.
        * GroupBy
            Expects `f` to be of type Callable[[Series], Series].
            Applies a python function over each group.

        Parameters
        ----------
        function
            Lambda/ function to apply.
        return_dtype
            Dtype of the output Series.
            If not set, the dtype will be
            ``polars.Unknown``.
        skip_nulls
            Don't apply the function over values
            that contain nulls. This is faster.
        pass_name
            Pass the Series name to the custom function
            This is more expensive.
        strategy : {'thread_local', 'threading'}
            This functionality is in `alpha` stage. This may be removed
            /changed without it being considered a breaking change.

            - 'thread_local': run the python function on a single thread.
            - 'threading': run the python function on separate threads. Use with
                        care as this can slow performance. This might only speed up
                        your code if the amount of work per element is significant
                        and the python function releases the GIL (e.g. via calling
                        a c function)

        Notes
        -----
        * Using ``apply`` is strongly discouraged as you will be effectively running
          python "for" loops. This will be very slow. Wherever possible you should
          strongly prefer the native expression API to achieve the best performance.

        * If your function is expensive and you don't want it to be called more than
          once for a given input, consider applying an ``@lru_cache`` decorator to it.
          With suitable data you may achieve order-of-magnitude speedups (or more).

        Warnings
        --------
        If ``return_dtype`` is not provided, this may lead to unexpected results.
        We allow this, but it is considered a bug in the user's query.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 2, 3, 1],
        ...         "b": ["a", "b", "c", "c"],
        ...     }
        ... )

        In a selection context, the function is applied by row.

        >>> df.with_columns(  # doctest: +SKIP
        ...     pl.col("a").apply(lambda x: x * 2).alias("a_times_2"),
        ... )
        shape: (4, 3)
        ┌─────┬─────┬───────────┐
        │ a   ┆ b   ┆ a_times_2 │
        │ --- ┆ --- ┆ ---       │
        │ i64 ┆ str ┆ i64       │
        ╞═════╪═════╪═══════════╡
        │ 1   ┆ a   ┆ 2         │
        │ 2   ┆ b   ┆ 4         │
        │ 3   ┆ c   ┆ 6         │
        │ 1   ┆ c   ┆ 2         │
        └─────┴─────┴───────────┘

        It is better to implement this with an expression:

        >>> df.with_columns(
        ...     (pl.col("a") * 2).alias("a_times_2"),
        ... )  # doctest: +IGNORE_RESULT

        In a GroupBy context the function is applied by group:

        >>> df.lazy().groupby("b", maintain_order=True).agg(
        ...     pl.col("a").apply(lambda x: x.sum())
        ... ).collect()
        shape: (3, 2)
        ┌─────┬─────┐
        │ b   ┆ a   │
        │ --- ┆ --- │
        │ str ┆ i64 │
        ╞═════╪═════╡
        │ a   ┆ 1   │
        │ b   ┆ 2   │
        │ c   ┆ 4   │
        └─────┴─────┘

        It is better to implement this with an expression:

        >>> df.groupby("b", maintain_order=True).agg(
        ...     pl.col("a").sum(),
        ... )  # doctest: +IGNORE_RESULT

        """
        # input x: Series of type list containing the group values
        from polars.utils.udfs import warn_on_inefficient_apply

        root_names = self.meta.root_names()
        if len(root_names) > 0:
            warn_on_inefficient_apply(function, columns=root_names, apply_target="expr")

        if pass_name:

            def wrap_f(x: Series) -> Series:  # pragma: no cover
                def inner(s: Series) -> Series:  # pragma: no cover
                    return function(s.alias(x.name))

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", PolarsInefficientApplyWarning)
                    return x.apply(
                        inner, return_dtype=return_dtype, skip_nulls=skip_nulls
                    )

        else:

            def wrap_f(x: Series) -> Series:  # pragma: no cover
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", PolarsInefficientApplyWarning)
                    return x.apply(
                        function, return_dtype=return_dtype, skip_nulls=skip_nulls
                    )

        if strategy == "thread_local":
            return self.map(wrap_f, agg_list=True, return_dtype=return_dtype)
        elif strategy == "threading":

            def wrap_threading(x: Series) -> Series:
                df = x.to_frame("x")

                n_threads = threadpool_size()
                chunk_size = x.len() // n_threads
                remainder = x.len() % n_threads
                if chunk_size == 0:
                    chunk_sizes = [1 for _ in range(remainder)]
                else:
                    chunk_sizes = [
                        chunk_size + 1 if i < remainder else chunk_size
                        for i in range(n_threads)
                    ]

                def get_lazy_promise(df: DataFrame) -> LazyFrame:
                    return df.lazy().select(
                        F.col("x").map(wrap_f, agg_list=True, return_dtype=return_dtype)
                    )

                # create partitions with LazyFrames
                # these are promises on a computation
                partitions = []
                b = 0
                for step in chunk_sizes:
                    a = b
                    b = b + step
                    partition_df = df[a:b]
                    partitions.append(get_lazy_promise(partition_df))

                out = [df.to_series() for df in F.collect_all(partitions)]
                return F.concat(out, rechunk=False)

            return self.map(wrap_threading, agg_list=True, return_dtype=return_dtype)
        else:
            ValueError(f"Strategy {strategy} is not supported.")
