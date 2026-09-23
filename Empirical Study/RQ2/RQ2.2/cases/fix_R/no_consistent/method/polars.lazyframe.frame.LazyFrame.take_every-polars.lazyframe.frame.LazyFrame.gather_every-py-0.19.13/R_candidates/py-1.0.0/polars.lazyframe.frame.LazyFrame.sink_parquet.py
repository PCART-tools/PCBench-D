    @unstable()
    def sink_parquet(
        self,
        path: str | Path,
        *,
        compression: str = "zstd",
        compression_level: int | None = None,
        statistics: bool | str | dict[str, bool] = True,
        row_group_size: int | None = None,
        data_pagesize_limit: int | None = None,
        maintain_order: bool = True,
        type_coercion: bool = True,
        predicate_pushdown: bool = True,
        projection_pushdown: bool = True,
        simplify_expression: bool = True,
        slice_pushdown: bool = True,
        no_optimization: bool = False,
    ) -> None:
        """
        Evaluate the query in streaming mode and write to a Parquet file.

        .. warning::
            Streaming mode is considered **unstable**. It may be changed
            at any point without it being considered a breaking change.

        This allows streaming results that are larger than RAM to be written to disk.

        Parameters
        ----------
        path
            File path to which the file should be written.
        compression : {'lz4', 'uncompressed', 'snappy', 'gzip', 'lzo', 'brotli', 'zstd'}
            Choose "zstd" for good compression performance.
            Choose "lz4" for fast compression/decompression.
            Choose "snappy" for more backwards compatibility guarantees
            when you deal with older parquet readers.
        compression_level
            The level of compression to use. Higher compression means smaller files on
            disk.

            - "gzip" : min-level: 0, max-level: 10.
            - "brotli" : min-level: 0, max-level: 11.
            - "zstd" : min-level: 1, max-level: 22.
        statistics
            Write statistics to the parquet headers. This is the default behavior.

            Possible values:

            - `True`: enable default set of statistics (default)
            - `False`: disable all statistics
            - "full": calculate and write all available statistics. Cannot be
              combined with `use_pyarrow`.
            - `{ "statistic-key": True / False, ... }`. Cannot be combined with
              `use_pyarrow`. Available keys:

              - "min": column minimum value (default: `True`)
              - "max": column maximum value (default: `True`)
              - "distinct_count": number of unique column values (default: `False`)
              - "null_count": number of null values in column (default: `True`)
        row_group_size
            Size of the row groups in number of rows.
            If None (default), the chunks of the `DataFrame` are
            used. Writing in smaller chunks may reduce memory pressure and improve
            writing speeds.
        data_pagesize_limit
            Size limit of individual data pages.
            If not set defaults to 1024 * 1024 bytes
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
        >>> lf.sink_parquet("out.parquet")  # doctest: +SKIP
        """
        lf = self._set_sink_optimizations(
            type_coercion=type_coercion,
            predicate_pushdown=predicate_pushdown,
            projection_pushdown=projection_pushdown,
            simplify_expression=simplify_expression,
            slice_pushdown=slice_pushdown,
            no_optimization=no_optimization,
        )

        if isinstance(statistics, bool) and statistics:
            statistics = {
                "min": True,
                "max": True,
                "distinct_count": False,
                "null_count": True,
            }
        elif isinstance(statistics, bool) and not statistics:
            statistics = {}
        elif statistics == "full":
            statistics = {
                "min": True,
                "max": True,
                "distinct_count": True,
                "null_count": True,
            }

        return lf.sink_parquet(
            path=normalize_filepath(path),
            compression=compression,
            compression_level=compression_level,
            statistics=statistics,
            row_group_size=row_group_size,
            data_pagesize_limit=data_pagesize_limit,
            maintain_order=maintain_order,
        )
