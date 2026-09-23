    def lazy(self) -> LazyFrame:
        """
        Start a lazy query from this point. This returns a `LazyFrame` object.

        Operations on a `LazyFrame` are not executed until this is requested by either
        calling:

        * :meth:`.fetch() <polars.LazyFrame.fetch>`
            (run on a small number of rows)
        * :meth:`.collect() <polars.LazyFrame.collect>`
            (run on all data)
        * :meth:`.describe_plan() <polars.LazyFrame.describe_plan>`
            (print unoptimized query plan)
        * :meth:`.describe_optimized_plan() <polars.LazyFrame.describe_optimized_plan>`
            (print optimized query plan)
        * :meth:`.show_graph() <polars.LazyFrame.show_graph>`
            (show (un)optimized query plan as graphviz graph)

        Lazy operations are advised because they allow for query optimization and more
        parallelization.

        Returns
        -------
        LazyFrame

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [None, 2, 3, 4],
        ...         "b": [0.5, None, 2.5, 13],
        ...         "c": [True, True, False, None],
        ...     }
        ... )
        >>> df.lazy()  # doctest: +ELLIPSIS
        <LazyFrame [3 cols, {"a": Int64 … "c": Boolean}] at ...>

        """
        return wrap_ldf(self._df.lazy())
