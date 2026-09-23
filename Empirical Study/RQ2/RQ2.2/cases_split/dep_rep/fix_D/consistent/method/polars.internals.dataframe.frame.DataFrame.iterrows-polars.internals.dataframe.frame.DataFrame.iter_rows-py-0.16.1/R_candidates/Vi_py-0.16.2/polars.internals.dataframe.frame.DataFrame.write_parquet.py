    def write_parquet(
        self,
        file: str | Path | BytesIO,
        *,
        compression: ParquetCompression = "zstd",
        compression_level: int | None = None,
        statistics: bool = False,
        row_group_size: int | None = None,
        use_pyarrow: bool = _PYARROW_AVAILABLE,
        pyarrow_options: dict[str, object] | None = None,
    ) -> None:
        """
        Write to Apache Parquet file.

        Parameters
        ----------
        file
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
            Write statistics to the parquet headers. This requires extra compute.
        row_group_size
            Size of the row groups in number of rows.
            If None (default), the chunks of the `DataFrame` are
            used. Writing in smaller chunks may reduce memory pressure and improve
            writing speeds. If None and ``use_pyarrow=True``, the row group size
            will be the minimum of the DataFrame size and 64 * 1024 * 1024.
        use_pyarrow
            Use C++ parquet implementation vs Rust parquet implementation.
            At the moment C++ supports more features.
        pyarrow_options
            Arguments passed to ``pyarrow.parquet.write_table``.

        Examples
        --------
        >>> import pathlib
        >>>
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3, 4, 5],
        ...         "bar": [6, 7, 8, 9, 10],
        ...         "ham": ["a", "b", "c", "d", "e"],
        ...     }
        ... )
        >>> path: pathlib.Path = dirpath / "new_file.parquet"
        >>> df.write_parquet(path)

        """
        if compression is None:
            compression = "uncompressed"
        if isinstance(file, (str, Path)):
            file = normalise_filepath(file)

        if use_pyarrow:
            tbl = self.to_arrow()
            data = {}

            for i, column in enumerate(tbl):
                # extract the name before casting
                name = f"column_{i}" if column._name is None else column._name

                data[name] = column

            tbl = pa.table(data)

            # do not remove this
            # needed below
            import pyarrow.parquet  # noqa: F401

            pa.parquet.write_table(
                table=tbl,
                where=file,
                row_group_size=row_group_size,
                compression=None if compression == "uncompressed" else compression,
                compression_level=compression_level,
                write_statistics=statistics,
                **(pyarrow_options or {}),
            )
        else:
            self._df.write_parquet(
                file, compression, compression_level, statistics, row_group_size
            )
