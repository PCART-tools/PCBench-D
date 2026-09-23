    def sink_ndjson(
        self,
        path: str | Path,
        *,
        maintain_order: bool = True,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        no_optimization: bool = False,
        slice_pushdown: bool = True,
    ) -> DataFrame:
        """
        Persists a LazyFrame at the provided path.

        This allows streaming results that are larger than RAM to be written to disk.

        Parameters
        ----------
        path
            File path to which the file should be written.
        maintain_order
            Maintain the order in which data is processed.
            Setting this to `False` will  be slightly faster.
        type_coercion
            Do type coercion optimization.
        predicate_pushdown
            Do predicate pushdown optimization.
        projection_pushdown
            Do projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        no_optimization
            Turn off (certain) optimizations.
        slice_pushdown
            Slice pushdown optimization.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> lf = pl.scan_csv("/path/to/my_larger_than_ram_file.csv")  # doctest: +SKIP
        >>> lf.sink_json("out.json")  # doctest: +SKIP

        """
        lf = self._set_sink_optimizations(
            type_coercion=type_coercion,
            predicate_pushdown=predicate_pushdown,
            projection_pushdown=projection_pushdown,
            simplify_expression=simplify_expression,
            no_optimization=no_optimization,
            slice_pushdown=slice_pushdown,
        )

        return lf.sink_json(path=path, maintain_order=maintain_order)
