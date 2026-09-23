    def inspect(self, fmt: str = "{}") -> LazyFrame:
        """
        Inspect a node in the computation graph.

        Print the value that this node in the computation graph evaluates to and pass on
        the value.

        Examples
        --------
        >>> lf = pl.LazyFrame({"foo": [1, 1, -2, 3]})
        >>> (
        ...     lf.with_columns(pl.col("foo").cum_sum().alias("bar"))
        ...     .inspect()  # print the node before the filter
        ...     .filter(pl.col("bar") == pl.col("foo"))
        ... )  # doctest: +ELLIPSIS
        <LazyFrame at ...>
        """

        def inspect(s: DataFrame) -> DataFrame:
            print(fmt.format(s))
            return s

        return self.map_batches(
            inspect, predicate_pushdown=True, projection_pushdown=True
        )
