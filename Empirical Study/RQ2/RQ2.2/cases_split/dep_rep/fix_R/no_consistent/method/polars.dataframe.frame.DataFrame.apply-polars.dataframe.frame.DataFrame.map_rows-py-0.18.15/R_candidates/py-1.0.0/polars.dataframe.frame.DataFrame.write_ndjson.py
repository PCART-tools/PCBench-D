    def write_ndjson(self, file: IOBase | str | Path | None = None) -> str | None:
        r"""
        Serialize to newline delimited JSON representation.

        Parameters
        ----------
        file
            File path or writable file-like object to which the result will be written.
            If set to `None` (default), the output is returned as a string instead.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...     }
        ... )
        >>> df.write_ndjson()
        '{"foo":1,"bar":6}\n{"foo":2,"bar":7}\n{"foo":3,"bar":8}\n'
        """

        def write_ndjson_to_string() -> str:
            with BytesIO() as buf:
                self._df.write_ndjson(buf)
                ndjson_bytes = buf.getvalue()
            return ndjson_bytes.decode("utf8")

        if file is None:
            return write_ndjson_to_string()
        elif isinstance(file, StringIO):
            ndjson_str = write_ndjson_to_string()
            file.write(ndjson_str)
            return None
        elif isinstance(file, (str, Path)):
            file = normalize_filepath(file)
            self._df.write_ndjson(file)
            return None
        else:
            self._df.write_ndjson(file)
            return None
