    def map_elements(
        self,
        function: Callable[[Series], Series] | Callable[[Any], Any],
        return_dtype: PolarsDataType | None = None,
        *,
        skip_nulls: bool = True,
        pass_name: bool = False,
        strategy: MapElementsStrategy = "thread_local",
    ) -> Self:
        """
        Map a custom/user-defined function (UDF) to each element of a column.

        .. warning::
            This method is much slower than the native expressions API.
            Only use it if you cannot implement your logic otherwise.

        The UDF is applied to each element of a column. Note that, in a GroupBy
        context, the column will have been pre-aggregated and so each element
        will itself be a Series. Therefore, depending on the context,
        requirements for `function` differ:

        * Selection
            Expects `function` to be of type ``Callable[[Any], Any]``.
            Applies a Python function to each individual value in the column.
        * GroupBy
            Expects `function` to be of type ``Callable[[Series], Any]``.
            For each group, applies a Python function to the slice of the column
            corresponding to that group.

        Parameters
        ----------
        function
            Lambda/function to map.
        return_dtype
            Dtype of the output Series.
            If not set, the dtype will be ``pl.Unknown``.
        skip_nulls
            Don't map the function over values that contain nulls (this is faster).
        pass_name
            Pass the Series name to the custom function (this is more expensive).
        strategy : {'thread_local', 'threading'}
            This functionality is considered experimental and may be removed/changed.

            - 'thread_local': run the python function on a single thread.
            - 'threading': run the python function on separate threads. Use with
              care as this can slow performance. This might only speed up
              your code if the amount of work per element is significant
              and the python function releases the GIL (e.g. via calling
              a c function)

        Notes
        -----
        * Using ``map_elements`` is strongly discouraged as you will be effectively
          running python "for" loops, which will be very slow. Wherever possible you
          should prefer the native expression API to achieve the best performance.

        * If your function is expensive and you don't want it to be called more than
          once for a given input, consider applying an ``@lru_cache`` decorator to it.
          If your data is suitable you may achieve *significant* speedups.

        * Window function application using ``over`` is considered a GroupBy context
          here, so ``map_elements`` can be used to map functions over window groups.

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

        The function is applied to each element of column `'a'`:

        >>> df.with_columns(  # doctest: +SKIP
        ...     pl.col("a").map_elements(lambda x: x * 2).alias("a_times_2"),
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

        Tip: it is better to implement this with an expression:

        >>> df.with_columns(
        ...     (pl.col("a") * 2).alias("a_times_2"),
        ... )  # doctest: +IGNORE_RESULT

        In a GroupBy context, each element of the column is itself a Series:

        >>> (
        ...     df.lazy().group_by("b").agg(pl.col("a")).collect()
        ... )  # doctest: +IGNORE_RESULT
        shape: (3, 2)
        ┌─────┬───────────┐
        │ b   ┆ a         │
        │ --- ┆ ---       │
        │ str ┆ list[i64] │
        ╞═════╪═══════════╡
        │ a   ┆ [1]       │
        │ b   ┆ [2]       │
        │ c   ┆ [3, 1]    │
        └─────┴───────────┘

        Therefore, from the user's point-of-view, the function is applied per-group:

        >>> (
        ...     df.lazy()
        ...     .group_by("b")
        ...     .agg(pl.col("a").map_elements(lambda x: x.sum()))
        ...     .collect()
        ... )  # doctest: +IGNORE_RESULT
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

        Tip: again, it is better to implement this with an expression:

        >>> (
        ...     df.lazy()
        ...     .group_by("b", maintain_order=True)
        ...     .agg(pl.col("a").sum())
        ...     .collect()
        ... )  # doctest: +IGNORE_RESULT

        Window function application using ``over`` will behave as a GroupBy
        context, with your function receiving individual window groups:

        >>> df = pl.DataFrame(
        ...     {
        ...         "key": ["x", "x", "y", "x", "y", "z"],
        ...         "val": [1, 1, 1, 1, 1, 1],
        ...     }
        ... )
        >>> df.with_columns(
        ...     scaled=pl.col("val").map_elements(lambda s: s * len(s)).over("key"),
        ... ).sort("key")
        shape: (6, 3)
        ┌─────┬─────┬────────┐
        │ key ┆ val ┆ scaled │
        │ --- ┆ --- ┆ ---    │
        │ str ┆ i64 ┆ i64    │
        ╞═════╪═════╪════════╡
        │ x   ┆ 1   ┆ 3      │
        │ x   ┆ 1   ┆ 3      │
        │ x   ┆ 1   ┆ 3      │
        │ y   ┆ 1   ┆ 2      │
        │ y   ┆ 1   ┆ 2      │
        │ z   ┆ 1   ┆ 1      │
        └─────┴─────┴────────┘

        Note that this function would *also* be better-implemented natively:

        >>> df.with_columns(
        ...     scaled=(pl.col("val") * pl.col("val").count()).over("key"),
        ... ).sort(
        ...     "key"
        ... )  # doctest: +IGNORE_RESULT

        """
        # input x: Series of type list containing the group values
        from polars.utils.udfs import warn_on_inefficient_map

        root_names = self.meta.root_names()
        if len(root_names) > 0:
            warn_on_inefficient_map(function, columns=root_names, map_target="expr")

        if pass_name:

            def wrap_f(x: Series) -> Series:  # pragma: no cover
                def inner(s: Series) -> Series:  # pragma: no cover
                    return function(s.alias(x.name))

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", PolarsInefficientMapWarning)
                    return x.map_elements(
                        inner, return_dtype=return_dtype, skip_nulls=skip_nulls
                    )

        else:

            def wrap_f(x: Series) -> Series:  # pragma: no cover
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", PolarsInefficientMapWarning)
                    return x.map_elements(
                        function, return_dtype=return_dtype, skip_nulls=skip_nulls
                    )

        if strategy == "thread_local":
            return self.map_batches(wrap_f, agg_list=True, return_dtype=return_dtype)
        elif strategy == "threading":

            def wrap_threading(x: Series) -> Series:
                def get_lazy_promise(df: DataFrame) -> LazyFrame:
                    return df.lazy().select(
                        F.col("x").map_batches(
                            wrap_f, agg_list=True, return_dtype=return_dtype
                        )
                    )

                df = x.to_frame("x")

                if x.len() == 0:
                    return get_lazy_promise(df).collect().to_series()

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

            return self.map_batches(
                wrap_threading, agg_list=True, return_dtype=return_dtype
            )
        else:
            ValueError(f"Strategy {strategy} is not supported.")
