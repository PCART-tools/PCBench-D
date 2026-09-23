    def write_parquet(
        self,
        file: str | Path | BytesIO,
        *,
        compression: ParquetCompression = "zstd",
        compression_level: int | None = None,
        statistics: bool = False,
        row_group_size: int | None = None,
        data_page_size: int | None = None,
        use_pyarrow: bool = False,
        pyarrow_options: dict[str, Any] | None = None,
    ) -> None:
        """
        Write to Apache Parquet file.

        Parameters
        ----------
        file
            File path or writeable file-like object to which the result will be written.
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
            Size of the row groups in number of rows. Defaults to 512^2 rows.
        data_page_size
            Size of the data page in bytes. Defaults to 1024^2 bytes.
        use_pyarrow
            Use C++ parquet implementation vs Rust parquet implementation.
            At the moment C++ supports more features.
        pyarrow_options
            Arguments passed to `pyarrow.parquet.write_table`.

            If you pass `partition_cols` here, the dataset will be written
            using `pyarrow.parquet.write_to_dataset`.
            The `partition_cols` parameter leads to write the dataset to a directory.
            Similar to Spark's partitioned datasets.

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

        We can use pyarrow with use_pyarrow_write_to_dataset=True
        to write partitioned datasets. The following example will
        write the first row to ../watermark=1/*.parquet and the
        other rows to ../watermark=2/*.parquet.

        >>> df = pl.DataFrame({"a": [1, 2, 3], "watermark": [1, 2, 2]})
        >>> path: pathlib.Path = dirpath / "partitioned_object"
        >>> df.write_parquet(
        ...     path,
        ...     use_pyarrow=True,
        ...     pyarrow_options={"partition_cols": ["watermark"]},
        ... )

        """
        if compression is None:
            compression = "uncompressed"
        if isinstance(file, (str, Path)):
            if pyarrow_options is not None and pyarrow_options.get("partition_cols"):
                file = normalize_filepath(file, check_not_directory=False)
            else:
                file = normalize_filepath(file)

        if use_pyarrow:
            tbl = self.to_arrow()
            data = {}

            for i, column in enumerate(tbl):
                # extract the name before casting
                name = f"column_{i}" if column._name is None else column._name

                data[name] = column

            tbl = pa.table(data)

            # do not remove this import!
            # needed below
            import pyarrow.parquet  # noqa: F401

            if pyarrow_options is None:
                pyarrow_options = {}
            pyarrow_options["compression"] = (
                None if compression == "uncompressed" else compression
            )
            pyarrow_options["compression_level"] = compression_level
            pyarrow_options["write_statistics"] = statistics
            pyarrow_options["row_group_size"] = row_group_size
            pyarrow_options["data_page_size"] = data_page_size

            if pyarrow_options.get("partition_cols"):
                pa.parquet.write_to_dataset(
                    table=tbl,
                    root_path=file,
                    **(pyarrow_options or {}),
                )
            else:
                pa.parquet.write_table(
                    table=tbl,
                    where=file,
                    **(pyarrow_options or {}),
                )

        else:
            self._df.write_parquet(
                file,
                compression,
                compression_level,
                statistics,
                row_group_size,
                data_page_size,
            )
