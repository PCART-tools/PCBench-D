    def write_avro(
        self,
        file: str | Path | IO[bytes],
        compression: AvroCompression = "uncompressed",
        name: str = "",
    ) -> None:
        """
        Write to Apache Avro file.

        Parameters
        ----------
        file
            File path or writable file-like object to which the data will be written.
        compression : {'uncompressed', 'snappy', 'deflate'}
            Compression method. Defaults to "uncompressed".
        name
            Schema name. Defaults to empty string.

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
        >>> path: pathlib.Path = dirpath / "new_file.avro"
        >>> df.write_avro(path)
        """
        if compression is None:
            compression = "uncompressed"
        if isinstance(file, (str, Path)):
            file = normalize_filepath(file)
        if name is None:
            name = ""

        self._df.write_avro(file, compression, name)
