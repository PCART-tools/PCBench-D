    def write_ipc_stream(
        self,
        file: str | Path | IO[bytes] | None,
        *,
        compression: IpcCompression = "uncompressed",
        future: bool | None = None,
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
        future
            Setting this to `True` will write Polars' internal data structures that
            might not be available by other Arrow implementations.

            .. warning::
                This functionality is considered **unstable**. It may be changed
                at any point without it being considered a breaking change.

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

        if compression is None:
            compression = "uncompressed"

        if future:
            issue_unstable_warning(
                "The `future` parameter of `DataFrame.write_ipc` is considered unstable."
            )
        if future is None:
            future = True

        self._df.write_ipc_stream(file, compression, future=future)
        return file if return_bytes else None  # type: ignore[return-value]
