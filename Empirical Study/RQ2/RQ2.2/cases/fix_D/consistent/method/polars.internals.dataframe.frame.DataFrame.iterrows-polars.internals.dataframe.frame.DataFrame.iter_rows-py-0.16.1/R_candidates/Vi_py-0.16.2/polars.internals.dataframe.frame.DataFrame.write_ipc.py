    def write_ipc(
        self,
        file: BinaryIO | BytesIO | str | Path,
        compression: IpcCompression = "uncompressed",
    ) -> None:
        """
        Write to Arrow IPC binary stream or Feather file.

        Parameters
        ----------
        file
            File path to which the file should be written.
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
        if compression is None:
            compression = "uncompressed"
        if isinstance(file, (str, Path)):
            file = normalise_filepath(file)

        self._df.write_ipc(file, compression)
