    @unstable()
    def sink_ndjson(
        self,
        path: str | Path,
        *,
        maintain_order: bool = True,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        no_optimization: bool = False,
    ) -> DataFrame:
        """
        Evaluate the query in streaming mode and write to an NDJSON file.

        .. warning::
            Streaming mode is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        This allows streaming results that are larger than RAM to be written to disk.

        Parameters
        ----------
        path
            File path to which the file should be written.
        maintain_order
            Maintain the order in which data is processed.
            Setting this to `False` will be slightly faster.
        type_coercion
            Do type coercion optimization.
        predicate_pushdown
            Do predicate pushdown optimization.
        projection_pushdown
            Do projection pushdown optimization.
        simplify_expression
            Run simplify expressions optimization.
        slice_pushdown
            Slice pushdown optimization.
        no_optimization
            Turn off (certain) optimizations.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> lf = pl.scan_csv("/path/to/my_larger_than_ram_file.csv")  # doctest: +SKIP
        >>> lf.sink_ndjson("out.ndjson")  # doctest: +SKIP
        """
        lf = self._set_sink_optimizations(
            type_coercion=type_coercion,
            predicate_pushdown=predicate_pushdown,
            projection_pushdown=projection_pushdown,
            simplify_expression=simplify_expression,
            slice_pushdown=slice_pushdown,
            no_optimization=no_optimization,
        )

        return lf.sink_json(path=path, maintain_order=maintain_order)
