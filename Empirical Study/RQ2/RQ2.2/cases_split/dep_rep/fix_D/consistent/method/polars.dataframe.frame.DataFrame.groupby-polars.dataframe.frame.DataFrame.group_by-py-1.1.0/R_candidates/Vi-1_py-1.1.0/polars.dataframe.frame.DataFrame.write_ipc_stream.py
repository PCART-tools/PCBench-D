    @deprecate_renamed_parameter("future", "compat_level", version="1.1")
    def write_ipc_stream(
        self,
        file: str | Path | IO[bytes] | None,
        *,
        compression: IpcCompression = "uncompressed",
        compat_level: CompatLevel | None = None,
    ) -> BytesIO | None:
        """
        Write to Arrow IPC record batch stream.

        See "Streaming format" in https://arrow.apache.org/docs/python/ipc.html.

        Parameters
        ----------
        file
            Path or writable file-like object to which the IPC record batch data will
            be written. If set to `None`, the output is returned as a BytesIO object.
        compression : {'uncompressed', 'lz4', 'zstd'}
            Compression method. Defaults to "uncompressed".
        compat_level
            Use a specific compatibility level
            when exporting Polars' internal data structures.

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
        >>> path: pathlib.Path = dirpath / "new_file.arrow"
        >>> df.write_ipc_stream(path)
        """
        return_bytes = file is None
        if return_bytes:
            file = BytesIO()
        elif isinstance(file, (str, Path)):
            file = normalize_filepath(file)

        if compat_level is None:
            compat_level = True  # type: ignore[assignment]
        elif isinstance(compat_level, CompatLevel):
            compat_level = compat_level._version  # type: ignore[attr-defined]

        if compression is None:
            compression = "uncompressed"

        self._df.write_ipc_stream(file, compression, compat_level)
        return file if return_bytes else None  # type: ignore[return-value]
