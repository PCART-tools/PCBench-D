    def write_ipc(
        self,
        file: BinaryIO | BytesIO | str | Path | None,
        compression: IpcCompression = "uncompressed",
    ) -> BytesIO | None:
        """
        Write to Arrow IPC binary stream or Feather file.

        See "File or Random Access format" in https://arrow.apache.org/docs/python/ipc.html.

        Parameters
        ----------
        file
            Path or writeable file-like object to which the IPC data will be
            written. If set to `None`, the output is returned as a BytesIO object.
        compression : {'uncompressed', 'lz4', 'zstd'}
            Compression method. Defaults to "uncompressed".

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
        >>> df.write_ipc(path)

        """
        return_bytes = file is None
        if return_bytes:
            file = BytesIO()
        elif isinstance(file, (str, Path)):
            file = normalize_filepath(file)

        if compression is None:
            compression = "uncompressed"

        self._df.write_ipc(file, compression)
        return file if return_bytes else None  # type: ignore[return-value]
