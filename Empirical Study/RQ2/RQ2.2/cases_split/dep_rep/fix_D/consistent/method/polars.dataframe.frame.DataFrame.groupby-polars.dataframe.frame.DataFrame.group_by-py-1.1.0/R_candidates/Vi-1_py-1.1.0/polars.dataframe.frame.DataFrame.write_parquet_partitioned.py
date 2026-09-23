    @unstable()
    def write_parquet_partitioned(
        self,
        path: str | Path,
        partition_by: str | Collection[str],
        *,
        chunk_size_bytes: int = 4_294_967_296,
        compression: ParquetCompression = "zstd",
        compression_level: int | None = None,
        statistics: bool | str | dict[str, bool] = True,
        row_group_size: int | None = None,
        data_page_size: int | None = None,
    ) -> None:
        """
        Write a partitioned directory of parquet files.

        Parameters
        ----------
        path
            Path to the base directory for the partitioned dataset.
        partition_by
            Columns to partition by.
        chunk_size_bytes
            Approximate size to split DataFrames within a single partition when
            writing. Note this is calculated using the size of the DataFrame in
            memory - the size of the output file may differ depending on the
            file format / compression.
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
            Size of the row groups in number of rows. Defaults to 512^2 rows.
        data_page_size
            Size of the data page in bytes. Defaults to 1024^2 bytes.
        """
        path = normalize_filepath(path, check_not_directory=False)
        partition_by = [partition_by] if isinstance(partition_by, str) else partition_by

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

        self._df.write_parquet_partitioned(
            path,
            partition_by,
            chunk_size_bytes,
            compression,
            compression_level,
            statistics,
            row_group_size,
            data_page_size,
        )
